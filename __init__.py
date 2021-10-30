import random
import string
from typing import List, Callable, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.requests import Request
from starlette.responses import Response

from app.core.adaptor.DbAdaptor import DbAdaptor
from app.core.adaptor.ListAdaptor import ListAdaptor
from app.core.module_class import Module, TableModule, ApiModule
from app.core.module_class.SecurityModule import SecurityModule
from app.modules.simple_key.table import SimpleKeyTable


class SimpleKey(ApiModule, SecurityModule, TableModule):
    # キーをチェックが必要かどうか、必要な時はデータベースが空きかどうかをチェックし
    # 空きだと最初の行を入れる
    is_need_to_check_key = True

    def _register_api_bp(self, bp: APIRouter):
        @bp.post('/create', summary='キーを作成する')
        def create(dba: DbAdaptor = Depends(DbAdaptor(SimpleKeyTable).dba),
                   name: str = Body(..., embed=True)):
            # ランダムなキーを作成
            key = ''.join(random.sample(string.ascii_letters + string.digits, 32))
            data = SimpleKeyTable(name=name, key=key)
            dba.add(data)
            return data

        @bp.delete('/delete')
        def delete(name: str,
                   dba: DbAdaptor = Depends(DbAdaptor(SimpleKeyTable).dba), ):
            return dba.delete_by(name=name)

        @bp.get('/ls')
        def ls(list_adaptor: ListAdaptor = Depends()):
            def map_filter(inp: dict):
                del inp['key']
                return inp

            return list_adaptor.search(SimpleKeyTable, map_filter)

    def get_table(self) -> list:
        return [SimpleKeyTable]

    def get_filters(self, module: Module) -> List[Callable]:
        def simple_filter(request: Request, response: Response,
                          dba: DbAdaptor = Depends(DbAdaptor(SimpleKeyTable).dba),
                          sec_key: Optional[str] = None):
            # データベースがまっ空きの時にadminというキーを作成
            if len(dba.read_all()) < 1:
                dba.add(SimpleKeyTable(name='admin', key='admin'))

            if sec_key is not None:
                # sec_keyがある時にクッキーに保存しておく
                response.set_cookie(key='sec_key', value=sec_key)
            elif 'sec_key' in request.cookies:
                # sec_keyがない時にリクエストから探す
                sec_key = request.cookies['sec_key']
            data = dba.read_by(key=sec_key)
            if data is None:
                # 権限不足の為わざとエラーを起こす
                raise HTTPException(403, 'forbidden')

        return [simple_filter]

    def _get_tag(self) -> str:
        return 'セキュリティキー作成ツール'

    def get_module_name(self) -> str:
        return 'simple_key'


simple_key = SimpleKey()

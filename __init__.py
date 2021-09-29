from typing import List, Callable, Optional

from fastapi import APIRouter

from app.core.module_class import Module, TableModule, ApiModule
from app.core.module_class.SecurityModule import SecurityModule
from app.modules.simple_key.table import SimpleKeyTable


class SimpleKey(ApiModule, SecurityModule, TableModule):
    # キーをチェックが必要かどうか、必要な時はデータベースが空きかどうかをチェックし
    # 空きだと最初の行を入れる
    is_need_to_check_key = True

    def _register_api_bp(self, bp: APIRouter):
        pass

    def get_table(self) -> list:
        return [SimpleKeyTable]

    def get_filters(self, module: Module) -> List[Callable]:
        def simple_filter(key: Optional[str] = None):
            ...

        return [simple_filter]

    def _get_tag(self) -> str:
        return 'セキュリティキー作成ツール'

    def get_module_name(self) -> str:
        return 'simple_key'


simple_key = SimpleKey()

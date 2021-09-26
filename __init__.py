from typing import List, Callable

from app.core.module_class import Module, TableModule
from app.core.module_class.SecurityModule import SecurityModule
from app.modules.simple_key.table import SimpleKeyTable


class SimpleKey(SecurityModule, TableModule):

    def get_table(self) -> list:
        return [SimpleKeyTable]

    def get_filters(self, module: Module) -> List[Callable]:
        def simple_filter(a: str):
            ...

        return [simple_filter]

    def _get_tag(self) -> str:
        return 'セキュリティキー作成ツール'

    def get_module_name(self) -> str:
        return 'simple_key'


simple_key = SimpleKey()

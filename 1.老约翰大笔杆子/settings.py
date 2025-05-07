from pathlib import Path
from nicegui import app
from dataclasses import dataclass,field
from typing import List


@dataclass
class NavItem:
    """
    每一个导航链接（包含在每一个expander下）
    """
    nav_name :str
    uri :str
    module_path :str = field(compare=False)

@dataclass 
class LeftNav:
    """
    每个tab页对应的左侧导航,包含2级
    """
    expander_name :str
    nav_items :List[NavItem]

@dataclass
class Section:
    """
    每个tab页
    """
    section_name :str
    uri :str
    module_path :str = field(compare=False)
    #left_navs :List[LeftNav] = field(compare=False)

############基本配置#################"
ROOT = Path(__file__).parent
#app.add_static_files("/asset", ROOT / "asset")


unrestricted_page_routes = {'/login'}

#####################################

#######Coze workflow########
coze_api_token = ""
 
coze_workflow_dice = {
    '大纲生成':"7498249529176588325",
    '文本生成':"7498249529176604709"
}


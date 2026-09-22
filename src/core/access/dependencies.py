from uuid import UUID
from collections.abc import Mapping

from src.core.enums import ProjectRole
from src.core.access.permissions import Permissions
from src.core.access.policies import Policies
from src.core.access.context import AccessContext

def get_access_context_for(

) -> AccessContext:
from rest_framework import routers
from .views import ProjectView, TeamMemberView, TaskView

router = routers.DefaultRouter()

router.register('proyect', ProjectView, 'proyect')
router.register('team_member', TeamMemberView, 'teammember')
router.register('task', TaskView, 'task')

urlpatterns = router.urls


from rest_framework import routers
from .views import ProjectView, TeamMemberView, TaskView

router = routers.DefaultRouter()

router.register('a', ProjectView, 'proyect')
router.register('b', TeamMemberView, 'teammember')
router.register('c', TaskView, 'task')

urlpatterns = router.urls


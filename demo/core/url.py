from rest_framework import routers

from core.views.mixins import ProjectViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, base_name='core')
router.register('tasks', TaskViewSet, base_name='core')


urlpatterns = router.urls


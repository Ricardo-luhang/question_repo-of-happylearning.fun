from apps.repo.models import Answers, Category, Questions
from tiku import settings
from apps.lib.repo_data import user_answer_data


def global_data(request):
    site = {}
    site['SITE_NAME'] = settings.SITE_NAME

    if request.user.is_authenticated:
        answers = Answers.objects.filter(user_id=request.user.id).count()
        question_num = Questions.objects.all().count()
        hot_question = Questions.objects.order_by('-answer_num')[:5]
        hot_user = Answers.objects.hot_user()
        user_data = user_answer_data(request.user)
    current_url = request.path
    category = Category.objects.all()

    return locals()

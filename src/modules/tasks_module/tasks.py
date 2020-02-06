from flask import Blueprint, url_for
from werkzeug.utils import redirect

from src.lib import (
    count_percentage_on_task,
    get_current_user,
    get_status_on_task,
    render,
)
from src.models import Subject, Task, TaskLink, TaskType

tasks = Blueprint("tasks", __name__, template_folder="templates")


@tasks.route("/<subj_name>/tasks")
def app_logged_in(subj_name):
    if get_current_user() is None:
        return redirect(url_for("index"))
    subject_list = list(Subject.find({"hidden": False}))
    subject = Subject.find_one({"name": subj_name})
    tasks_list = []
    raw_tasks = TaskType.find({"subject": subject.id})
    for t in raw_tasks:
        tasks_list.append(
            {
                "number": int(t.number),
                "compete_percentage": count_percentage_on_task(t),
                "points": t.points,
                "status": get_status_on_task(t),
            }
        )
    for t in raw_tasks:
        tasks_list.append(
            {"number": 1, "compete_percentage": 100, "points": 1, "status": 0,}
        )
    return render(
        "tasks.html",
        title="Задания",
        header_label="Все задания первой части",
        current_subj=subj_name,
        current_mode="tasks",
        subject_list=subject_list,
        tasks_list=tasks_list,
    )


@tasks.route("/<subj_name>/task/<int:task_id>")
def task_theory(subj_name, task_id):
    subject_list = list(Subject.find({"hidden": False}))
    subject = Subject.find_one({"name": subj_name})
    task_type = TaskType.find_one({"subject": subject.id, "number": str(task_id)})
    return render(
        "task-theory.html",
        title="Задание",
        header_label="Теория по заданию",
        current_subj=subj_name,
        current_mode="tasks",
        subject_list=subject_list,
        task_id=task_id,
        cods=list(task_type.cods),
        task_description=task_type.description
        # task_description="В задании нужно прочитать текст и выбрать варианты ответов, которые наиболее точно передают "
        # "его главную мысль. В данном задании всегда два варианта ответа. За правильный даётся один "
        # "первичный балл.",
    )


@tasks.route("/<subj_name>/task/<int:task_id>/practice")
def task_practice(subj_name, task_id):
    if get_current_user() is None:
        return redirect(url_for("index"))
    user = get_current_user()
    subject = Subject.find_one({"name": subj_name})
    subject_list = list(Subject.find({"hidden": False}))
    task_type = TaskType.find_one({"subject": subject.id, "number": str(task_id)})
    tasks = []
    raw_tasks = Task.find({"task_type": task_type.id})
    for task in raw_tasks:
        tl = TaskLink.find_one({"task": task.id, "user": user.id})
        text = None
        if task.text is not None:
            text = task.text.fetch().body
            print(text)
        tasks.append(
            {
                "number": task_type.number,
                "description": eval('"' + task.description + '"'),
                "text": text,
                "options": task.options,
                "done": tl.done if tl else False,
                "answers": task.answers,
                "explanation": task.explanation
            }
        )
    return render(
        "task-practice.html",
        title="Задания",
        header_label="Практика задания",
        current_subj=subj_name,
        current_mode="tasks",
        subject_list=subject_list,
        tasks=[
            {
                "number": "1",
                "description": "Укажите два предложения, в которых верно передана ГЛАВНАЯ информация, содержащаяся в тексте. Запишите номера этих предложений.",
                "text": "(1) Индоиранское общество подразделялось на три класса: вожди и жрецы, воины и простые земледельцы и пастухи. (2) … классовое деление получило свое отражение и в религии: каждому из перечисленных классов принадлежали свои особые боги. (3) Асуры были связаны с первым, высшим классом вождей и жрецов. (4) В жертву богам приносили кровь животных, огонь и перебродивший сок некоего растения (саумы). (5) Эти жертвоприношения, призванные обеспечить благополучие человека и продление его рода (что всегда играло важную роль в погребальных обрядах), и позволяли ему как бы заранее вкусить бессмертие через опьянение саумой.",
                "options": [
                    "1) Классовое деление индоиранского общества получило отражение в религии, к примеру, с высшим классом вождей и жрецов были связаны асуры.",
                    "2) Чтобы обеспечить благополучие человека и продление его рода, богам приносили в жертву кровь животных, огонь и перебродивший сок саумы.",
                    "3) Асуры, одни из богов индоиранской традиционной религии, были связаны с высшим из трех классов индоиранского общества – с классом вождей и жрецов.",
                    "4) Каждому из трёх классов индоиранского общества соответствовали свои боги, при этом богам для обеспечения благополучия человека принято было приносить в жертву кровь животных, огонь и перебродивший сок саумы.",
                    "6) Перебродивший сок саумы, кровь животных и огонь приносили в жертву индоиранским богам, соответствующим социальному классу, к которому относился человек, чтобы обеспечить продление его рода и его благополучие."
                ],
                "answers": ["45"],
                "explanation": "Так как вариант 1) передаёт содержание только первых трех предложений. Вариант 2), напротив, передаёт содержание только предложений 4-5. Вариант 3) полностью соответствует третьему предложению."
            },
            {
                "number": "1",
                "description": "Укажите два предложения, в которых верно передана ГЛАВНАЯ информация, содержащаяся в тексте. Запишите номера этих предложений.",
                "text": "(1) Индоиранское общество подразделялось на три класса: вожди и жрецы, воины и простые земледельцы и пастухи. (2) … классовое деление получило свое отражение и в религии: каждому из перечисленных классов принадлежали свои особые боги. (3) Асуры были связаны с первым, высшим классом вождей и жрецов. (4) В жертву богам приносили кровь животных, огонь и перебродивший сок некоего растения (саумы). (5) Эти жертвоприношения, призванные обеспечить благополучие человека и продление его рода (что всегда играло важную роль в погребальных обрядах), и позволяли ему как бы заранее вкусить бессмертие через опьянение саумой.",
                "options": [
                    "1) Классовое деление индоиранского общества получило отражение в религии, к примеру, с высшим классом вождей и жрецов были связаны асуры.",
                    "2) Чтобы обеспечить благополучие человека и продление его рода, богам приносили в жертву кровь животных, огонь и перебродивший сок саумы.",
                    "3) Асуры, одни из богов индоиранской традиционной религии, были связаны с высшим из трех классов индоиранского общества – с классом вождей и жрецов.",
                    "4) Каждому из трёх классов индоиранского общества соответствовали свои боги, при этом богам для обеспечения благополучия человека принято было приносить в жертву кровь животных, огонь и перебродивший сок саумы.",
                    "6) Перебродивший сок саумы, кровь животных и огонь приносили в жертву индоиранским богам, соответствующим социальному классу, к которому относился человек, чтобы обеспечить продление его рода и его благополучие."
                ],
                "answers": ["45"],
                "explanation": "Так как вариант 1) передаёт содержание только первых трех предложений. Вариант 2), напротив, передаёт содержание только предложений 4-5. Вариант 3) полностью соответствует третьему предложению."
            }
        ]
    )

current_task = 0;
current_cods = [];
codNumberClickActive = true;

function passwordReestablish(obj) {
    let objInfo = obj.getBoundingClientRect();
    let windowObjInfo = $(".password-reestablish-window__wrapper")[0].getBoundingClientRect();
    $(".password-reestablish-window__wrapper").css({
        "top": objInfo.y - objInfo.height - windowObjInfo.height + "px",
        "left": objInfo.x + objInfo.width / 2 - windowObjInfo.width / 2 + "px",
        "z-index": "1",
        "opacity": "1"
    });

}

function sendReestablishEmail() {
    $(".password-reestablish-window__wrapper").css({
        "top": "-9999px",
        "z-index": "-3",
        "opacity": "0"
    });
}

$(document).on("click", (event) => {
    if (!$(event.target).hasClass("prwe")) {
        $(".password-reestablish-window__wrapper").css({
            "top": "-9999px",
            "z-index": "-3",
            "opacity": "0"
        });
    }
});

$(document).on("click", (event) => {
    if ($(event.target).hasClass("task-block-status")){
        event.preventDefault();
        let objCoords = $(event.target)[0].getBoundingClientRect();
        let windowCoords = $(".status-change-window")[0].getBoundingClientRect();
        current_task = $(event.target).data("task-number");
        $(".status-change-window").css({
            "top": objCoords.y - windowCoords.height / 2 + objCoords.height / 2 + $(window).scrollTop() + "px",
            "left": objCoords.x - windowCoords.width + "px",
            "z-index": "2",
            "opacity": "1"
        });
    }
    if(!($(event.target)[0].classList.value.includes("status-change")) && !($(event.target)[0].classList.value.includes("task-block-status"))) {
        $(".status-change-window").css({
            "top": "0",
            "left": "-9999px",
            "z-index": "-2",
            "opacity": "0"
        });
    }
});

function changeTaskStatus(obj) {
    let subject_name = $(".all-tasks-block").data("subject-name");
    $.post("/api/change_status", {
        subject_name: subject_name,
        task_number: current_task,
        new_status: $(obj).data("status")
    });
    $("[data-task-number=\"" + current_task + "\"]")[0].src = "../../static/img/" + $(obj).data("status") + "_status_icon.png";
    $(".status-change-window").css({
        "top": "0",
        "left": "-9999px",
        "z-index": "-2",
        "opacity": "0"
    });
}

$(document).on("click", (event) => {
    if ($(event.target).hasClass("practice")) {
        event.preventDefault();
        let objInfo = $(event.target)[0].getBoundingClientRect();
        let windowInfo = $(".test-creation-window")[0].getBoundingClientRect();
        $(".test-creation-window").css({
            "top": objInfo.top + objInfo.height / 2 - windowInfo.height / 2 + "px",
            "left": "150px",
            "z-index": "2",
            "opacity": "1"
        });
    }
    if (!$(event.target)[0].classList.value.includes("test-creation") && !$(event.target).hasClass("practice")) {
        $(".test-creation-window").css({
            "top": "0px",
            "left": "-9999px",
            "z-index": "-2",
            "opacity": "0"
        });
    }
});

function createTest() {
    let numbers = $(".test-creation-window-input")[0].value.split(" ")
    console.log(numbers);
}

$(document).on("click", (event) => {
    if ($(event.target).hasClass("cod-number") && codNumberClickActive) {
        let number = parseInt($(event.target)[0].innerHTML);
        if ($(event.target).hasClass("active")) {
            $(event.target)[0].classList.remove("active");
            current_cods = current_cods.filter(num => num !== number)
        }
        else {
            $(event.target)[0].classList.add("active");
            current_cods.push(number)
        }

        codNumberClickActive = false;
        setTimeout(() => codNumberClickActive = true, 100);
        let objChildrens = $(".learn-page-blocks").children();

        for (let i=0; i < objChildrens.length; i++) {
            $(objChildrens[i]).css({"display": "block"});
        }
        if (current_cods.length > 0) {
            for (let i=0; i < objChildrens.length; i++) {
                if (!(current_cods.includes(parseInt($(objChildrens[i]).data("number"))))) {
                    $(objChildrens[i]).css({"display": "none"});
                }
            }
        }
    }
});

function checkTaskAnswer(obj) {
    let rightAnswers = String($(obj).data("answers")).split(" ");
    let userAnswer = $(obj).prev()[0].value;
    if (rightAnswers.includes(userAnswer)) {
        $(obj).prev().css({"border": "2px solid #2ecc71"});
        $.post("/api/task_done", {
            task_id: $(obj).data("id")
        });
    }
    else {
        $(obj).prev().css({"border": "2px solid #f74a5a"});
    }
}

function showTaskAnswer(obj) {
    if ($(obj)[0].innerHTML === "Показать ответ") {
        $(obj).parent().next().slideDown(200);
        $(obj)[0].innerHTML = "Скрыть ответ";
    }
    else {
        $(obj).parent().next().slideUp(200);
        $(obj)[0].innerHTML = "Показать ответ";
    }
}

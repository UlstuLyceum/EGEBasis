function confirmEmail() {
    $(".signup-window__content").css({"width": "375px", "color": "#fff"});
    $(".signup-window__content")[0].innerHTML = "<p class=\"signup-window-text\">На указанную вами почту было выслано письмо, следуйте инструкциям, написанным в нём, чтобы завершить регистрацию.</p><a href=\"/login\" class=\"signup-window-end-signup-button\">Завершить</a>";
}

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
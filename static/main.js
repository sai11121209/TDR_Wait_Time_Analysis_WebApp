$(function () {
    $('head').append(
        '<style type="text/css">#container { display: none; } #fade, #loader { display: block; }</style>'
    );

    jQuery.event.add(window, "load", function () { // 全ての読み込み完了後に呼ばれる関数
        var pageH = $("#container").height();

        $("#fade").css("height", pageH).delay(900).fadeOut(800);
        $("#loader").delay(600).fadeOut(300);
        $("#container").css("display", "block");
    });
    $('#sideMenuButton').on('click', function () {
        $('#sideMenuButton, #menu, #menuNav').toggleClass('menuOpen');
    });
});
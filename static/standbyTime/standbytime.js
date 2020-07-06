$(function () {
    $("#today-table").hide();
    $("#yesterday-table").hide();
    $("#today-table-button").on('click', () => {
        $("#today-table").slideToggle();
    });
    $("#yesterday-table-button").on('click', () => {
        $("#yesterday-table").slideToggle();
    });
});
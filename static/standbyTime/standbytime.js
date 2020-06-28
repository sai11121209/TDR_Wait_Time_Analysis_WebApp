$(function () {
    let xdatas = document.getElementById('figure_xdatas').value;
    let ydatas = document.getElementById('figure_ydatas').value;
    new Chart(document.getElementById("ct-chart"), {
        type: "line",
        data: {
            labels: [ydatas],
            datasets: [
                {
                    label: "待ち時間",
                    data: [xdatas],
                    backgroundColor: [
                        "rgb(255, 99, 132)",
                        "rgb(54, 162, 235)",
                        "rgb(255, 205, 86)"
                    ]
                }
            ]
        }
    });
});
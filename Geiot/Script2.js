$(function () {
    $("div#home_content").append('<h2>request</h2><ul id="request_contents"></ul >')
    $.getJSON("sample_json2.json", (data) => {
        let innerdata = data["request_recipi"]
        Object.keys(innerdata).forEach(function (elem) {
            let list_elem = '';
            for (i of innerdata[elem]["fav_ingredeints"]) {
                list_elem += ("<li class='fav_ingredeints_list'>" + i + "</li>")
            };
            $.getJSON("users.json", (user_data) => {
                $('ul#request_contents').append('<div class="request_recipis"><p> ユーザー名 : ' + user_data[innerdata[elem]["userID"]]["name"] + '            性別  : ' + user_data[innerdata[elem]["userID"]]["gender"] + '</p><p>レシピ名   :   <label>' + innerdata[elem]["recipi"] + '</label><p>入れて欲しい材料</p><ul>' + list_elem + '</ul><p>備考</p><textarea readonly class="contents_textarea">' + innerdata[elem]["information"] + '</textarea></div>');
            });
        });
    });
    Drew_graph();
    $.ajax({
        url: 'Python/match.py',
        type: 'post'
    }).done(function (data) {
        $("div#mealmeating_content").append(data)
    }).fail(function () {
        console.log('failed');
    });
});
function Drew_graph() {
    var ctx = $("#followsgraph");
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['3ヶ月前', '２ヶ月前', '１ヶ月前', '現在', '1ヶ月後', '2ヶ月後', '3ヶ月後'],
            datasets: [
                {
                    label: 'フォロワー数',
                    data: [35, 34, 37, 35, 34, 35, 34, 25],
                    borderColor: "rgba(255,0,0,1)",
                    backgroundColor: "rgba(0,0,0,0)"
                },
            ],
        },
        options: {
            title: {
                display: true,
                text: 'フォロワー推移'
            },
            scales: {
                yAxes: [{
                    ticks: {
                        suggestedMax: 40,
                        suggestedMin: 0,
                        stepSize: 10,
                        callback: function (value, index, values) {
                            return value + '人'
                        }
                    }
                }]
            },
        }
    });
}
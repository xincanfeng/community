// JavaScript source code
$(function () {
    $("div#home_content").append('<h2>recipi</h2> <ul id="fav_contents" class="x_scroll_list"></ul >')
    $.getJSON("sample_json.json", (data) => {
        Object.keys(data["recipis"]).forEach(function (key) {
            $('ul#fav_contents').append("<li class='item'><div class='content'><img src='" + data["recipis"][key] + "'><p>" + key + "</p></div ></li>")
        });
    });
});
function UpIngredients() {
    $("ul#fav_Ingredients").append("<input type='text' class='Ingredients_text'>");
};
function DownIngredients() {
    $("ul#fav_Ingredients input:last-child").remove();
};
function Ingredients_All_Clear() {
    $("ul#fav_Ingredients input").remove();
};

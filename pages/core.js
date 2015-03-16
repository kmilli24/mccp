/**
 * Created by drazisil on 3/16/15.
 */
var lastUpdateTimeStamp = '';

function handleInput(cmd) {
    $.post("/cmd", {cmd: cmd, source: 'web'});
    $("#cmd").val("");
    return false;
}

var myAjaxCall = function () {
    $.ajax({
        type: "GET",
        url: '/term',
        dataType: "json",
        success: function (json) {
            if (json.timestamp > lastUpdateTimeStamp) {
                var term = $('#term-display');
                term.html('');
                $.each(json.output, function (index, value) {
                    term.append(value + "<br>");
                });
                lastUpdateTimeStamp = json.timestamp;
                term.scrollTop(term[0].scrollHeight);
            }
        }
    })
};

window.onload = function () {
    var ResInterval = window.setInterval('myAjaxCall()', 1000); // 60 seconds

};

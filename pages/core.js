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
    //noinspection JSUnusedGlobalSymbols
    $.ajax({
        type: "GET",
        url: '/term',
        dataType: "json",
        success: function (json) {
            if (json.timestamp > lastUpdateTimeStamp) {
                var term = $('#term-display');
                var tmpReply = '';
                term.html('');
                //noinspection JSUnresolvedVariable
                $.each(json.output, function (index, value) {
                    tmpReply += value + "<br>";
                });
                term.html(tmpReply);
                lastUpdateTimeStamp = json.timestamp;
                //noinspection JSValidateTypes
                term.scrollTop(term[0].scrollHeight);
            }
        }
    })
};

window.onload = function () {
    window.setInterval('myAjaxCall()', 1000); // 60 seconds

};

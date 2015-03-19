/**
 * Created by drazisil on 3/16/15.
 */
var lastUpdateTimeStamp = '';

function handleInput(cmd) {
    $.post("/cmd", {cmd: cmd, source: 'web'});
    var div_cmd;
    div_cmd = $("#cmd");
    div_cmd.val("");
    div_cmd.focus();
    return false;
}

function updateStatus(status) {
    var statusIcon = $("#controlStatus");
    switch (status) {
        case "stopped":
            statusIcon.css('backgroundColor', 'red');
            break;
        case 'running':
            statusIcon.css('backgroundColor', 'lime');
            break;
        case 'starting':
        case 'stopping':
        case 'restarting':
            statusIcon.css('backgroundColor', 'yellow');
            break
    }
    statusIcon.attr('title', status);

}

var myAjaxCall = function () {
    //noinspection JSUnusedGlobalSymbols
    $.ajax({
        type: "GET",
        url: '/term',
        dataType: "json",
        success: function (json) {
            if (json.timestamp > lastUpdateTimeStamp) {
                updateStatus(json.status);
                var term = $('#term-display');
                if (term.length > 0) {
                    //noinspection JSUnresolvedVariable
                    var tmpReply = json.output.join("<br>");
                    term.html(tmpReply.toString());
                    lastUpdateTimeStamp = json.timestamp;
                    //noinspection JSValidateTypes
                    term.scrollTop(term[0].scrollHeight);
                }
            }
        }
    })
};

window.onload = function () {
    window.setInterval('myAjaxCall()', 1000); // 60 seconds
    $("#cmd").focus();

};

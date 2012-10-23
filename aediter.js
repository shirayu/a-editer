
/*
    author  : Yuta Hayashibe
    license : GPL v3
*/

$(function(){
    var MyCount = 0;
    var prevMyText = '';

    function adjust_area_size(){
        $("#mytext").css(
            {width:$(window).width()-30, height:$(window).height()-60}
            );
    };

    function save(){
        if($("#isNew").val() == ''){
            return
        };

        $("body").append(
            "<div class='loading' id='loading' style='display:block; position:fixed; top:0px; left:0px;'><img src='roller.gif' alt='loading'/></div>"
            );
        var mydata = {
            'cmd' : 'save' ,
            'f' : $('#mytitle').val() ,
            'mytext' : $('#mytext').val() ,
            'encoding' :  $('#encoding').val()
        };
        ++MyCount;
        $.ajax('', {
            dataType: 'json',
            type: 'post',
            data: mydata,
            mytext: $('#mytext').val(),
            success: function(data) {
                --MyCount;
                if (MyCount ==0){ //if not 0, others are sending
                    $("#loading").remove();
                };
                if (data.status = 'ok'){
                    prevMyText = this.mytext;
                    refresh()
                }
                else{
                    alert('error'); //FIXME
                };
            }
        });
    };

    function refresh_title(){
        document.title = $("#isNew").val() + "[" + $("#mytitle").val() + "][" + $("#encoding").val() + "]";
        $('#notice').html( document.title );
    };
    
    function init(){
        refresh_title();
        adjust_area_size();
        prevMyText = $('#mytext').val();
    };
    function refresh(){
        var newMyText = $('#mytext').val();
        if (newMyText != prevMyText){
            $('#isNew').val("*");
        }
        else{
            $('#isNew').val("");
        };
        refresh_title();
    };

    ////////
    var window_resize = function(e){
       adjust_area_size();
    };

    var onkeydown   = function(e) {
        if ( e.ctrlKey && e.keyCode == 83){ //ctrl + s
            save();
            return false;
        }
        else if ( e.ctrlKey && e.keyCode == 82){ //ctrl + r
            return false;
        }
        else if(e.keyCode == 9) { //TAB
            var REP = '    ';
            var text_elem = (document.activeElement || window.getSelection().focusNode);
            var left = text_elem.selectionStart;
            var right = text_elem.selectionEnd;
            var oldtext = $(text_elem).val();
            $(text_elem).val( oldtext.substr(0, left) + REP + oldtext.substr(right));
            text_elem.selectionStart = left + REP.length;
            text_elem.selectionEnd = left + REP.length;

            if(e.preventDefault) {
                e.preventDefault();
            }
            return false;
        };
    }

    var onkeyup   = function(e) {
        refresh();
    };

    $("body").keydown( onkeydown );
    $("body").keyup( onkeyup );
    $( window ).resize(window_resize);
    window.onbeforeunload = function(){  
        if($("#isNew").val() != ''){
            return "Are you sure to leave?\nYour chage will be lost.";   
        };
    } 
    ////////

    init();
});


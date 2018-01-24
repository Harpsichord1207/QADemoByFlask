function timetojump(second,jumpurl){
    var timer= document.getElementById('timer');
    timer.innerHTML=second;
    if(--second>0){
        setTimeout("timetojump("+second+",'"+jumpurl+"')",1000);
        }
    else{
        location.href=jumpurl;
        }
    }

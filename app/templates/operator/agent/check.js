    function ischeckall(){
    $("#checkall").change(function(){
        let otherCheckList = $("div tbody input[type='checkbox']");
        let checkAllStatus = $("#checkall").prop("checked");
        otherCheckList.prop("checked",checkAllStatus);
    });
    }

    function listencheckbox(){
    $('div table tbody input[type="checkbox"]').on('change',function(){
    let total = $('div table tbody input[type="checkbox"]').length;
    let active = $('div table tbody input[type="checkbox"]:checked').length;
    $('table thead input[type="checkbox"]').get(0).checked = (total === active);
    });
    }

    window.onload = function(){
    var i = 0;
    trlength = $('tbody tr').length;
    for(i;i<trlength;i++){
        numtd = $('tbody tr')[i].cells[1];
        numtd.innerText = i + 1;
    }
    };
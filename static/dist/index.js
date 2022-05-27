
function optBtnHandler(e){
    var optType = $(this).attr("opttype");
    var dataId = $(this).attr("dataId");
    if(optType == "editUser"){
        var username = $(this).attr("username");
        $("#edit_user_id").val(dataId);
        $("#edit_user_fullname").val(username);
        var myModal = new bootstrap.Modal(document.getElementById('edit_user_modal'), {
          keyboard: false
        });
        myModal.show();
    }else if(optType == "deleteUser"){
    var username = $(this).attr("username");
        var isconfirm = confirm("您确定删除用户“"+username+"”吗？")
        if(isconfirm){
            $.post('/user',
                {
                    "type": 'delete',
                    "id":dataId
                },
                function (callback) {
                    window.location.reload();
                })
        }
    }
}
// 车流量的编辑与删除按钮
function optBtnHandler2(e){
    var optType = $(this).attr("opttype");
    var dataId = $(this).attr("dataId");
    if(optType=="editCar"){
        console.log("点击了编辑车流量");
        var direction  =$(this).attr("direction");
        var flow = $(this).attr("flow");
        var time = $(this).attr("time");

        $("#edit_car_id").val(dataId);

        $("#edit_car_direction").val(direction);
        $("#edit_car_flow").val(flow);
        $("#edit_car_time").val(time);
        console.log(dataId,direction,flow,time);
        var myModal = new bootstrap.Modal(document.getElementById('edit_car_modal'), {
          keyboard: false
        });
        myModal.show();
    }else if(optType=="deleteCar"){
        console.log("删除车流量")
        var isconfirm = confirm("您确定删除该记录吗？")
        if(isconfirm){
            $.post('/car',
                {
                    "type": 'delete',
                    "id":dataId
                },
                function (callback) {
                    window.location.reload();
                })
        }
    }
}
//知识的编辑与删除 按钮
function optBtnHandler3(e){
    var optType = $(this).attr("opttype");
    var dataId = $(this).attr("dataId");
    if(optType=="editRule"){
        console.log("点击了编辑知识");
        var E  =$(this).attr("E");
        var H = $(this).attr("H");
        var CFE = $(this).attr("CFE");
        var CFHE = $(this).attr("CFHE");
        $("#edit_rule_id").val(dataId);

        $("#edit_rule_E").val(E);
        $("#edit_rule_H").val(H);
        $("#edit_rule_CFE").val(CFE);
        $("#edit_rule_CFHE").val(CFHE);
        console.log(dataId,E,H,CFE,CFHE);
        var myModal = new bootstrap.Modal(document.getElementById('edit_rule_modal'), {
          keyboard: false
        });
        myModal.show();
    }else if(optType=="deleteRule"){
        console.log("删除知识")
        var isconfirm = confirm("您确定删除这条知识吗？")
        if(isconfirm){
            $.post('/rule',
                {
                    "type": 'delete',
                    "id":dataId
                },
                function (callback) {
                    window.location.reload();
                })
        }
    }
}

function optBtnHandler4(e){
    $("#result_weather_rain").val($(this).attr("weatherRain"));
    $("#result_weather_snow").val($(this).attr("weatherSnow"));
    $("#result_weather_wind").val($(this).attr("weatherWind"));
    $("#result_car_numbers").val($(this).attr("carNumbers"));
    $("#result_base_pass_time").val($(this).attr("basePassTime"));
    $("#result_public_time").val($(this).attr("publicTime"));
    $("#result_allocated_public_time").val($(this).attr("publicAllocatedTimes"));
    $("#result_weather_add_time").val($(this).attr("weatherAddTimes"));

    var myModal = new bootstrap.Modal(document.getElementById('see_result'), {
      keyboard: false
    });
    myModal.show();
}
function onAddUserClickHandler(e){
    var myModal = new bootstrap.Modal(document.getElementById('add_user_modal'), {
      keyboard: false
    })
    myModal.show()
}

function onAddUserSubmitClickHandler(e){
    var myModal = new bootstrap.Modal(document.getElementById('add_user_modal_show_btn'), {
      keyboard: false
    })
    var fullname = $("#fullname").val();
    $.post('/user',
        {
            "type": 'add',
            "username": $("#fullname").val()
        },
        function (callback) {
            window.location.reload();
        })


    myModal.hide()
}

function onEidtUserSubmitClickHandler(e){
    var myModal = new bootstrap.Modal(document.getElementById('add_user_modal_show_btn'), {
      keyboard: false
    })
    var fullname = $("#edit_user_fullname").val();
    var id = $("#edit_user_id").val();
    $.post('/user',
        {
            "type": 'edit',
            "username": fullname,
            "id":id
        },
        function (callback) {
            window.location.reload();
        })


    myModal.hide()
}

/*车流量*/
function onAddCarClickHandler(e){
    var myModal = new bootstrap.Modal(document.getElementById('add_car_modal'), {
      keyboard: false
    })
    myModal.show()
}

function onAddCarSubmitClickHandler(e){
    var myModal = new bootstrap.Modal(document.getElementById('add_car_modal_show_btn'), {
      keyboard: false
    })
    var direction = $("#direction").val();
    var flow = $("#flow").val();
    var time = $("#time").val();
    $.post('/car',
        {
            "type": 'add',
            "direction": $("#direction").val(),
            "flow": $("#flow").val(),
            "time": $("#time").val()
        },
        function (callback) {
            window.location.reload();
        })


    myModal.hide()
}

function onEidtCarSubmitClickHandler(e){
    console.log("开始执行修改车流量！！！")
   var myModal = new bootstrap.Modal(document.getElementById('add_car_modal_show_btn'), {
     keyboard: false
   })
    var id = $("#edit_car_id").val();
   var direction = $("#edit_car_direction").val();
   var flow = $("#edit_car_flow").val();
   var time = $("#edit_car_time").val();
   console.log('修改后的车流量为：\n');
   console.log(direction,flow,time);
   console.log("以post方法发送数据");
   $.post('/car',
       {
           "type": 'edit',
           "id":id,
           "direction": direction,
           "flow":flow,
           "time":time,
       },
       function (callback) {
           window.location.reload();
       })
   myModal.hide()
}

// 可信度知识
function onAddRuleClickHandler(e){
    var myModal = new bootstrap.Modal(document.getElementById('add_rule_modal'), {
      keyboard: false
    })
    myModal.show()
}
// 天气
function onAddWeatherClickHandler(e){
    var myModal = new bootstrap.Modal(document.getElementById('add_weather'), {
      keyboard: false
    })
    myModal.show()
}
function onAddWeatherSubmitClickHandler(e){
    var myModal = new bootstrap.Modal(document.getElementById('add_weather'), {
      keyboard: false
    })
    var rain = $("#add_rain").val();
    var snow = $("#add_snow").val();
    var wind = $("#add_wind").val();
    $.post('/weather',
        {
            "type": 'add',
            "rain": rain,
            "snow": snow,
            "wind": wind
        },
        function (callback) {
            window.location.reload();
        })


    myModal.hide()
}
function onAddRuleSubmitClickHandler(e){
    var myModal = new bootstrap.Modal(document.getElementById('add_rule_modal_show_btn'), {
      keyboard: false
    })
    var E = $("#E").val();
    var H = $("#H").val();
    var CFE = $("#CFE").val();
    var CFHE = $("#CFHE").val();
    $.post('/rule',
        {
            "type": 'add',
            "E": E,
            "H": H,
            "CFE": CFE,
            "CFHE":CFHE
        },
        function (callback) {
            window.location.reload();
        })


    myModal.hide()
}

function onEidtRuleSubmitClickHandler(e){
    console.log("开始执行修改知识！！！")
   var myModal = new bootstrap.Modal(document.getElementById('add_rule_modal_show_btn'), {
     keyboard: false
   })
    var id = $("#edit_rule_id").val();
    var E = $("#edit_rule_E").val();
   var H = $("#edit_rule_H").val();
   var CFE = $("#edit_rule_CFE").val();
   var CFHE = $("#edit_rule_CFHE").val();
   console.log('修改后的知识为：\n');
   console.log(E,H,CFE,CFHE);
   console.log("以post方法发送数据");

   // var E  =$(this).attr("E");
   //  var H = $(this).attr("H");
   //  var CFE = $(this).attr("CFE");
   //  var CFHE = $(this).attr("CFHE");
   //  $("#edit_rule_id").val(dataId);
   //
   //  $("#edit_rule_E").val(E);
   //  $("#edit_rule_H").val(H);
   //  $("#edit_rule_CFE").val(CFE);
   //  $("#edit_rule_CFHE").val(CFHE);
   //  console.log(dataId,E,H,CFE,CFHE);
   $.post('/rule',
        {
            "type": 'edit',
            "id":id,
            "E": E,
            "H": H,
            "CFE": CFE,
            "CFHE":CFHE
        },
       function (callback) {
           window.location.reload();
       })
   myModal.hide()
}

// handleAddFuzzyBtnClick Show AddFuzzyModal.
function handleAddFuzzyBtnClick() {
    var myModal = new bootstrap.Modal(document.getElementById('add_fuzzy_modal'), {
      keyboard: false
    })

    myModal.show()
}

// handleSubmitFuzzyBtnClick handle click 'submit' button in AddFuzzyModal.
function handleSubmitFuzzyBtnClick() {
   var myModal = new bootstrap.Modal(document.getElementById('add_fuzzy_modal'), {
     keyboard: false
   })
    let create_fuzzy_name = $('#create_fuzzy_name').val()
    let create_fuzzy_input_var_desc = $('#create_fuzzy_input_var_desc').val()
    let create_fuzzy_output_var_desc = $('#create_fuzzy_output_var_desc').val()
    let create_fuzzy_input_output_relation = $('#create_fuzzy_input_output_relation').val()

   $.post('/fuzzy',
    {
        create_fuzzy_name: create_fuzzy_name,
        create_fuzzy_input_var_desc: create_fuzzy_input_var_desc,
        create_fuzzy_output_var_desc: create_fuzzy_output_var_desc,
        create_fuzzy_input_output_relation: create_fuzzy_input_output_relation,
    },
   function (callback) {
       window.location.reload();
   })
   myModal.hide()
}



$(document).ready(function(){
    // 用户
    $('#add_user_modal_show_btn').click(onAddUserClickHandler);
    $("#add_user_submit").click(onAddUserSubmitClickHandler);
    $("#edit_user_submit").click(onEidtUserSubmitClickHandler);
    // 车流量
    $('#add_car_modal_show_btn').click(onAddCarClickHandler);
    $("#add_car_submit").click(onAddCarSubmitClickHandler);
    $("#edit_car_submit").click(onEidtCarSubmitClickHandler);
    // 可信度知识
    $('#add_rule_modal_show_btn').click(onAddRuleClickHandler);
    $('#add_rule_submit').click(onAddRuleSubmitClickHandler);
     $("#edit_rule_submit").click(onEidtRuleSubmitClickHandler);
    $(".optbtn").click(optBtnHandler);
    $(".optbtn2").click(optBtnHandler2);
    $(".optbtn3").click(optBtnHandler3);
    $(".optbtn4").click(optBtnHandler4);
    // 模糊知识管理
    $('#add_fuzzy_btn').click(handleAddFuzzyBtnClick);
    $('#add_fuzzy_submit').click(handleSubmitFuzzyBtnClick);
    $('#set_weather_button').click(onAddWeatherClickHandler);
    $('#add_weather_submit').click(onAddWeatherSubmitClickHandler);
})


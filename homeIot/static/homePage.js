
$(document).ready(function(){




$(".light-toggle-btn").click(function(){
  var id = $(this).attr('id');
  var id = id.split('-');
  var light = id[0];
  var state = id[1];
  toggleLight(light , parseInt(state));  
  $(this).closest('.btn-group').children().removeClass("active");
  $(this).addClass("active");
});


//jcf.replaceAll();


});



function openSettings(){
    return;
}

function navPage(element, destination){
  container  = element.closest('.pageContainer');
  $(container).css('display','none');
  $('#'+destination).css('display','block');
  loadSettings();
}

function toggleLight(light,state){
    var data = {}
    data.state = state;
    data.light = light;
    $.ajax({
      type: "POST",
      url: "API/changeLightSchedule",
      data : JSON.stringify(data),
      ContentType : "application/json",
      success: function(status) {
          console.log(status);
      }
    });
}

function updateCycleSettings(){

  data = {'sensorThreshold' : $("#sensorThreshold").val(),
          'drainTime' : $("#drainTime").val(),
          'errorTime' : $("#waterRunInTime").val(),
          'dryTime' :  $("#airrationTime").val()
        };

  $.ajax({
      type: "POST",
      url: "API/updateCycleSettings",
      data : JSON.stringify(data),
      ContentType : "application/json",
      success: function(status) {
          console.log(status);
      }
    });

}

function loadSettings(){
      $.ajax({
      type: "POST",
      url: "API/loadSettings",
      ContentType : "application/json",
      success: function(data) {
          console.log(data);
          $("#sensorThreshold").val(data.threshold);
          $("#drainTime").val(data.drainTime);
          $("#waterRunInTime").val(data.errorTime);
          $("#airrationTime").val(data.dryTime);
          $("#dcPulse").val(data.dcPulse);
      }
    });

}


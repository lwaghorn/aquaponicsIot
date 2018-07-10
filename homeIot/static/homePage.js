
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

passwordKeyUps()

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
      url: "API/toggleLight",
      data : JSON.stringify(data),
      ContentType : "application/json",
      success: function(status) {
          console.log(status);
      }
    });
}


function updateCycleSettings(){

  data = {'threshold' : $("#sensorThreshold").val(),
          'drainTime' : $("#drainTime").val()*1000,
          'errorTime' : $("#waterRunInTime").val()*1000,
          'dryTime' :  $("#airrationTime").val()*1000,
          'password': $("#password").val(),
          'dcPulse' : $('#dcPulse').val()*1000
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
          lightStatuses = data.lightStatuses
          lightStatuses.forEach(function(status){
                $('#'+status['lightName']+"-"+status['mode']).addClass('active');
          });
          configuration = data.configuration
          $("#sensorThreshold").val(configuration.threshold);
          $("#drainTime").val(configuration.drainTime/1000);
          $("#waterRunInTime").val(configuration.errorTime/1000);
          $("#airrationTime").val(configuration.dryTime/1000);
          $("#dcPulse").val(configuration.dcPulse/1000);
      }
    });
}


function passwordKeyUps(){
  $('#password').keypress(function (e) {
  console.log('23');
  if (e.which == 13) {
    updateCycleSettings();
    return false;
  }
  else{
     //Implement password feedback thing
  }
});
}
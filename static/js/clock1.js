(function () {

  var clockElement = document.getElementById( "clock" );
  var wakeuptime = document.getElementById( "clock" );

  function updateClock ( clock ) {
    clock.innerHTML = new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'});
    if(wakeuptime == clockElement){
    	function submitform() {   document.myform.submit(); }
    }
  }

  setInterval(function () {
      updateClock( clockElement );
  }, 1000);


}());
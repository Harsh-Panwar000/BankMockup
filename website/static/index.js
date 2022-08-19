function toggle_display(){
  var ele = document.getElementsByClassName('.addAccountButton'); 
  if (ele.value == "Add new checking account"){
    ele.value = "No account needed";
  }else{
    ele.value="Add new checking account"
  }
}

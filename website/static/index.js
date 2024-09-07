/**
 * @description Changes the value of a form input element with class `.addAccountButton`.
 * It alternates between "Add new checking account" and "No account needed" based on
 * the current value, effectively toggling its display state.
 */
function toggle_display(){
  var ele = document.getElementsByClassName('.addAccountButton'); 
  if (ele.value == "Add new checking account"){
    ele.value = "No account needed";
  }else{
    ele.value="Add new checking account"
  }
}

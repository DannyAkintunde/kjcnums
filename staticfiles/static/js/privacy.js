const selectall = document.getElementById('selectall')
const userlist = document.getElementById('users')
const users = userlist.getElementsByClassName('user')
const search = document.querySelector('#search')
const form_users_list = document.querySelector('#div_id_users')
const form_users = form_users_list.getElementsByTagName('option')


const init = () => {
    for (let i = 0; i < users.length; i++) {
        const element = users[i];
        const form_user = form_users[i];
        element.getElementsByTagName("input")[0].checked = form_user.selected
        element.getElementsByTagName("input")[0].addEventListener('input',(e) => {
            if (e.target.checked === false){
                selectall.checked = false
            }
            check_func(e)
        })
    }
}

init()

function check_func(e){
    for (let i = 0; i < users.length; i++) {
        const user = users[i];
        const form_user = form_users[i];
        if (user.getElementsByTagName("label")[0].textContent === form_user.textContent){
            form_user.selected = user.getElementsByTagName("input")[0].checked;
            console.log(form_user.textContent,form_user.selected)
        }
        
    }
}

const deselectAll = () => {
  for (let i = 0; i < users.length; i++) {
    const element = users[i];
    const form_user = form_users[i];
    // Uncheck each checkbox
    element.getElementsByTagName("input")[0].checked = false;
    // Unselect each option in the <select> element
    form_user.selected = false;
  }
  // Uncheck the "select all" checkbox
  selectall.checked = false;
};

selectall.addEventListener('input',(e)=>{
    for (let i = 0; i < users.length; i++) {
        const element = users[i];
        const form_user = form_users[i];
        element.getElementsByTagName('input')[0].checked = e.target.checked;
        if (
            element.getElementsByTagName("label")[0].textContent ===
            form_user.textContent
        ) {
            form_user.selected =e.target.checked;
            console.log(form_user.textContent, form_user.selected);
        }
    }
})

const search_func = (e) => {
  quary = e.target.value.toLowerCase();
  for (let i = 0; i < users.length; i++) {
    const element = users[i];
    content = element.getElementsByTagName("label")[0];
    if (!content.textContent.toLowerCase().includes(quary)) {
      element.classList.add("hidden");
      console.log(element.classList);
    } else {
      element.classList.remove("hidden");
      console.log(element.classList);
    }
  }
};
search.addEventListener('input',search_func)

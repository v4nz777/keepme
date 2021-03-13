document.addEventListener('DOMContentLoaded', ()=> {

    // for mobile
    const menu = document.querySelector('.menu');
    const menuContents = document.querySelector('.menu-contents');
    menuContents.style.display = 'none';
    menu.addEventListener('click', (e)=> {
        if(menuContents.style.display == 'none'){
            menuContents.style.display = 'grid'; 
        }else{
            menuContents.style.display = 'none'; 
        }
        
    })

    //open/close notification bar
    const notifButton = document.querySelector('#notif-button');
    const notifBarOuter = document.querySelector('#notif-bar-outer');
    const notifCount_ = document.querySelector('#notif-count');
    notifBarOuter.style.display = 'none';
        notifButton.addEventListener('click', () => {
            if(notifBarOuter.style.display == 'none'){
                notifBarOuter.style.display = 'block';
                localStorage.setItem('last-notif-count', notifCount_.innerText);
                notifCount_.innerText = "";
            }else{
                notifBarOuter.style.display = 'none';
                notifCount_.innerText = localStorage.getItem("last-notif-count");
            }
        })
    
    // load contents of notifications
    
    //var ntcounts1 = 0
    //var ntcounts2 = 0

    
    //setInterval(()=>{
        loadBorrowNotifs()
        loadReturnNotifs()
        miniLoadBorrowNotifs()
        miniLoadReturnNotifs()
   // }, 5000)

})


function viewNotifCounts(result){
    if(result.notif_counts >= 1){
        const notifCount = document.querySelector('#notif-count');
        notifCount.innerText = result.notif_counts;
    }  
}

function loadReturnNotifs(){
    fetch('/api/api_return_requests/')
    .then(response => response.json())
    .then(result => {

        //const dbCounts = Object.keys(result).length;
        //const storedCounts = parseInt(localStorage.getItem("last-notif-count"))
        //if(dbCounts != storedCounts)    
        result.forEach(res => {   
            const notifBar = document.querySelector('#notif-bar');
            const eachNotif = document.createElement('div');
            eachNotif.setAttribute('id', `notifID-${res.context_thing_id}` );
            eachNotif.setAttribute('class', `notif-content` );
            if(res.done == false){
                eachNotif.innerHTML = `<span>
                                            <span id="ntfBorrower-${res.context_thing_id}">
                                            ${res.context_borrower}
                                            </span>
                                            wants to return:
                                            <span id="ntf-${res.context_thing_id}">
                                            ${res.context_thing}<br>
                                            </span>
                                        </span>

                                        <div class="sbs_buttons">
                                            <button id="request-${res.context_thing_id}-agree-return">agree</button>
                                            <button id="request-${res.context_thing_id}-reject-return">reject</button>
                                        </div><hr>`;
            }
            notifBar.append(eachNotif);
            buttonPostAgreeOrReject(res);
        })
    })
}

function miniLoadReturnNotifs(){
    fetch('/api/api_return_requests/')
    .then(response => response.json())
    .then(result => {
   
        result.forEach(res => {   
            const notifBar = document.querySelector('#notifAreaMini');
            const eachNotif = document.createElement('div');
            eachNotif.setAttribute('id', `miniNotifID-${res.context_thing_id}` );
            eachNotif.setAttribute('class', `notif-content` );
            if(res.done == false){
                eachNotif.innerHTML = `<span>
                                            <span id="mini-ntfBorrower-${res.context_thing_id}">
                                            ${res.context_borrower}
                                            </span>
                                            wants to return:
                                            <span id="mini-ntf-${res.context_thing_id}">
                                            ${res.context_thing}<br>
                                            </span>
                                        </span>

                                        <div class="sbs_buttons">
                                            <button id="mini-request-${res.context_thing_id}-agree-return">agree</button>
                                            <button id="mini-request-${res.context_thing_id}-reject-return">reject</button>
                                        </div><hr>`;
            }
            notifBar.append(eachNotif); 
            buttonPostAgreeOrReject(res);
        })
    })
}



function loadBorrowNotifs(){
    fetch('/api/api_borrow_requests/')
    .then(response => response.json())
    .then(result => {
        result.forEach(res => {
        

            const notifBar = document.querySelector('#notif-bar');
            const eachNotif = document.createElement('div');
            eachNotif.setAttribute('id', `notifID-${res.context_thing_id}` );
            eachNotif.setAttribute('class', `notif-content` );
            if(res.done == false){
                eachNotif.innerHTML = `<span>
                                            <span id="ntfBorrower-${res.context_thing_id}">
                                            ${res.context_borrower}
                                            </span>
                                        wants to borrow:
                                            <span id="ntf-${res.context_thing_id}">
                                            ${res.context_thing}<br>
                                            Return Date: ${res.context_return}
                                            </span>
                                        </span>

                                        <div class="sbs_buttons">
                                            <button id="request-${res.context_thing_id}-agree-borrow">agree</button>
                                            <button id="request-${res.context_thing_id}-reject-borrow">reject</button>
                                        </div><hr>`;
            }
            notifBar.append(eachNotif);
            buttonPostAgreeOrReject(res);
        })
    })
}


function miniLoadBorrowNotifs(){
    fetch('/api/api_borrow_requests/')
    .then(response => response.json())
    .then(result => {
        
        result.forEach(res => {   
            const notifBar = document.querySelector('#notifAreaMini');
            const eachNotif = document.createElement('div');
            eachNotif.setAttribute('id', `miniNotifID-${res.context_thing_id}` );
            eachNotif.setAttribute('class', `notif-content` );
            if(res.done == false){
                eachNotif.innerHTML = `<span>
                                            <span id="mini-ntfBorrower-${res.context_thing_id}">
                                            ${res.context_borrower}
                                            </span>
                                            wants to return:
                                            <span id="mini-ntf-${res.context_thing_id}">
                                            ${res.context_thing}<br>
                                            </span>
                                        </span>

                                        <div class="sbs_buttons">
                                            <button id="mini-request-${res.context_thing_id}-agree-borrow">agree</button>
                                            <button id="mini-request-${res.context_thing_id}-reject-borrow">reject</button>
                                        </div><hr>`;
            }
            notifBar.append(eachNotif);
            
            buttonPostAgreeOrReject(res);
        })
    })
}


function buttonPostAgreeOrReject(res){
    // FUNCTIONALITY OF THE BUTTONS
    const actionAgree_B = document.querySelector(`#request-${res.context_thing_id}-agree-borrow`);
    const actionReject_B = document.querySelector(`#request-${res.context_thing_id}-reject-borrow`);
    const miniActionAgree_B = document.querySelector(`#mini-request-${res.context_thing_id}-agree-borrow`);
    const miniActionReject_B = document.querySelector(`#mini-request-${res.context_thing_id}-reject-borrow`);

    const actionAgree_R = document.querySelector(`#request-${res.context_thing_id}-agree-return`);
    const actionReject_R = document.querySelector(`#request-${res.context_thing_id}-reject-return`);
    const miniActionAgree_R = document.querySelector(`#mini-request-${res.context_thing_id}-agree-return`);
    const miniActionReject_R = document.querySelector(`#mini-request-${res.context_thing_id}-reject-return`);

    //BORROW AGREE
    

    
        if(actionAgree_B){
            actionAgree_B.addEventListener('click', ()=> {
                respondNotif('agree_or_reject_trans', res.context_thing_id, 'agree');              
            })
        }
        if(miniActionAgree_B){
            miniActionAgree_B.addEventListener('click', ()=> {
                respondNotif('agree_or_reject_trans', res.context_thing_id, 'agree');
                
            })
        }
        //BORROW REJECT
        if(actionReject_B){
            actionReject_B.addEventListener('click', ()=> {
                respondNotif('agree_or_reject_trans', res.context_thing_id, 'reject');          
            })
        }
        if(miniActionReject_B){
            miniActionReject_B.addEventListener('click', ()=> {
                respondNotif('agree_or_reject_trans', res.context_thing_id, 'reject');           
            })
        }

        //RETURN AGREE
        if(actionAgree_R){
            actionAgree_R.addEventListener('click', ()=> {
                respondNotif('agree_or_reject_ret', res.context_thing_id, 'agree');
            })
        }
        if(miniActionAgree_R){
            miniActionAgree_R.addEventListener('click', ()=> {
                respondNotif('agree_or_reject_ret', res.context_thing_id, 'agree');              
            })
        }
        //RETURN REJECT
        if(actionReject_R){
            actionReject_R.addEventListener('click', ()=> {
                respondNotif('agree_or_reject_ret', res.context_thing_id, 'reject');  
            })
        }
        if(miniActionReject_R){
            miniActionReject_R.addEventListener('click', ()=> {
                respondNotif('agree_or_reject_ret', res.context_thing_id, 'reject');
            })
        }
    
}


function respondNotif(url_name, id, action){
    fetch(`/${url_name}/${id}`, {
        method: 'POST',
        body: JSON.stringify({
            id: id,
            action: action,
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
        
        

            if(result.lastnotif_count == 0){
                localStorage.setItem('last-notif-count', '');
            }else{
                localStorage.setItem('last-notif-count', result.lastnotif_count);
            }

            location.reload();

            
        
    })
}




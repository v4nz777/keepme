document.addEventListener('DOMContentLoaded', ()=> {


    // Lets define Logged user for comparisons
    const requestUser = document.querySelector('#requestUser').innerHTML.replace(/\s+/g, '');

    // Load currentUser's Profile
    const currentUser = document.querySelector('#currentUser').innerHTML.replace(/\s+/g, '');
    loadProfile(currentUser);

    // Compare Users
    addButtonView(requestUser, currentUser);

    //change avatar
    if(currentUser == requestUser){
        changeAvatar();
    }
    

    // close object view
    document.querySelectorAll('.blurr_other').forEach((blurred) => {
        closeObject(blurred);
    });


});

////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////      FUNCTIONS       ///////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////

// Load User's Details and things
function loadProfile(user){
    fetch(`/api/profile/${user}`)
    .then(response => response.json())
    .then(result => {
        const eMail = document.querySelector('#email');
        const addRess = document.querySelector('#address');
        const avatarImage = document.querySelector('#avatar')


        // Adding Details to Profile
        eMail.innerHTML = result.email;
        addRess.innerHTML = result.address;
        avatarImage.src = result.avatar;
        //REPUTATION SYSTEM
        reputationSystem(result);

        // THINGS
        result.stash_objects.forEach((pk,i) => {
            setTimeout(loadOBJ, i * 300, pk);
        });  
        // NOTIFICATIONS
        viewNotifCounts(result)

        result.stash_objects.forEach(pk => {
            const returnButton = document.querySelector(`#request-${pk}-return`)
            if(returnButton){
                returnButton.addEventListener('click', ()=> {
                    attemptReturn(pk)  
                })
            }
        })
    })
}

function attemptReturn(pk) {
    fetch(`/return_borrowed/${pk}`,{
        method: 'POST',
        body: JSON.stringify({  
            thing_id: pk,
        })
    })
        .then(response => response.json())
        .then(result => {
            console.log(result)
            const returnButton = document.querySelector(`#request-${result.thing_id}-return`);
            const returnButtonContainer = document.querySelector(`#borrow-button-${result.thing_id}-container`);

            if(result.success && returnButton && returnButtonContainer){                
                returnButton.innerText = 'Return Pending...';
                returnButton.disabled = true;
                
                returnButtonContainer.setAttribute('class', 'form-submit-disabled flex_end_button')
            }
        })
}




function loadOBJ(thingID){

    fetch(`/api/api_for_each_object/${thingID}`)
    .then(response => response.json())
    .then(result => {
        //const objectChanged = document.querySelector(`#thingID-${thingID}`)
        //objectChanged.remove();
        //THE CONTENT -EACH

        createContentContainer(result);
    
        // inside CONTAINER
        createInsideOfObject(result);        
    })
}




// for lend function
function lendObject(idNum) {
    const transactButton = document.querySelector(`#lend-button-${idNum}`);
    const transactButtonContainer = document.querySelector(`#lend-button-${idNum}-container`);
    const transactButtonCancel = document.querySelector(`#lend-button-${idNum}-cancel`);
    const transactForm = document.querySelector(`#lend-option-${idNum}`);
    //initially hide this option
    transactForm.style.display = 'none';
    // then show when clicked
    transactButton.addEventListener('click', ()=> {
        if(transactForm.style.display == 'none') {
            transactForm.style.display = 'block';
            transactButtonContainer.style.display = 'none';
        }    
    });
    transactButtonCancel.addEventListener('click', ()=> {
        if(transactForm.style.display == 'block') {
            transactForm.style.display = 'none';
            transactButtonContainer.style.display = 'block';
        }    
    });
}

// for lend/borrow function
function borrowObject(idNum) {
    const transactButton = document.querySelector(`#borrow-button-${idNum}`);
    const transactButtonContainer = document.querySelector(`#borrow-button-${idNum}-container`);
    const transactButtonCancel = document.querySelector(`#borrow-button-${idNum}-cancel`);
    const transactForm = document.querySelector(`#borrow-option-${idNum}`);
    if(transactForm && transactButton && transactButtonCancel){
        //initially hide this option
        transactForm.style.display = 'none';

        // then show when clicked
        transactButton.addEventListener('click', ()=> {
            if(transactForm.style.display == 'none') {
                transactForm.style.display = 'block';
                transactButtonContainer.style.display = 'none';
            }    
        });
        transactButtonCancel.addEventListener('click', ()=> {
            if(transactForm.style.display == 'block') {
                transactForm.style.display = 'none';
                transactButtonContainer.style.display = 'block';
            }
        });
    }  
}




//  for opening object view
function openObject(object){
    document.querySelector(`#object-${object}`).style.display = 'flex';
}
//for closing object view
function closeObject(blurred) {
    blurred.addEventListener('click', event => {
        if(blurred !== event.target) return;
        blurred.style.display = 'none';
    })
}

    


function changeAvatar() {
    // compare the viewed user and logged user to ensure not editing other user
    const avatar = document.querySelector('#avatar');
    const avatarEditButton = document.querySelector('#avatarEditBox');
    //avatarEditButton.style.display = 'none';
    avatar.addEventListener('mouseover', ()=> {
        avatarEditButton.style.display = 'flex';
    });
    avatar.addEventListener('mouseout', ()=> {
        avatarEditButton.style.display = 'none';
    });

    const avatarInput = document.querySelector('#avatarInput');
    avatarInput.addEventListener('change', ()=> {
        avatarEditButton.style.display = 'none';
        document.querySelector('#avatarEdit').style.display = 'none';
        const avatarSubmit = document.querySelector('#avatarSubmit');
        avatarSubmit.style.display = 'block';
        avatarSubmit.style.position = 'absolute';
        avatarSubmit.style.left = '20%';
        avatarSubmit.style.top = '40%';

    });
}



function addButtonView(requestUser, currentUser){
    if(requestUser == currentUser){
        // ADD New Item Modal Functions 
        const modal_addNewItem = document.querySelector('#add_new_form');
        const blurr_addNewItem = document.querySelector('#blurr_addNewItem');
            // if clicked open 'add new' modal
            document.querySelector('#addNewItem').addEventListener('click', ()=> {
                blurr_addNewItem.style.display = 'flex';
                blurr_addNewItem.style.justifyContent = 'center';
                modal_addNewItem.style.display = 'block';
            });
            // if clicked, close 'add new' modal
            document.querySelector('#close_addNewItem').addEventListener('click', ()=> {
                blurr_addNewItem.style.display = 'none';
                modal_addNewItem.style.display = 'none';
            });
            // Display button only to logged in user
            document.querySelector('#addNewItem').style.display = 'flex';
        } else{
            // Hide button if not current logged user
            document.querySelector('#addNewItem').style.display = 'none';
        }
}



// For manipulating rep stars
function reputationSystem(result){
    const rep0 = document.querySelector("#rep-0");
    const rep1 = document.querySelector("#rep-1");
    const rep2 = document.querySelector("#rep-2");
    const rep3 = document.querySelector("#rep-3");
    const rep4 = document.querySelector("#rep-4");
    const rep5 = document.querySelector("#rep-5");

    if(result.reputation == 5){
        rep5.style.display = "flex";
    }else if(result.reputation == 4){
        rep4.style.display = "flex";
    }else if(result.reputation == 3){
        rep3.style.display = "flex";
    }else if(result.reputation == 2){
        rep2.style.display = "flex";
    }else if(result.reputation == 1){
        rep1.style.display = "flex";
    }else if(result.reputation == 0){
        rep0.style.display = "flex";
    }
}


////////////////////////////////// FOR OBJECT DOM CREATION /////////////////////////////////
function createInsideOfObject(thing) {
    const newThing = document.querySelector(`#thingID-${thing.pk}`);
    createConatentTitle(thing, newThing);
    const loggedUser = document.querySelector('#requestUser').innerText;
    if(loggedUser == thing.owner && thing.borrowed == true){
        createBadge_Lent(thing, newThing);
   
    }else if(loggedUser != thing.owner && thing.borrowed == true){   
        createBadge_Borrowed(thing, newThing)
        
    }
    
    if(loggedUser == thing.owner){
        // then apply function to hide or display lend option
        lendObject(thing.pk);  
    }else{
        // then apply function to hide or display borrow option
        borrowObject(thing.pk);
    }  
}


function createContentContainer(thing) {

    const create_newThing = document.createElement('div');
            create_newThing.setAttribute('class', 'content-container');
            create_newThing.setAttribute('id', `thingID-${thing.pk}`);
            create_newThing.setAttribute('onclick', `openObject(${thing.pk})`);

            // add the created element to the LIST of THINGS
            document.querySelector('.contents-contents').append(create_newThing); 
}



function createBadge_Lent(thing, container) { 
    //ADD BADGE: lent
        const badge_cont = document.createElement('div');
        badge_cont.setAttribute('id', `badgeFor-${thing.pk}`);

        const viewedUserProfile = document.querySelector('#currentUser').innerText;
        if(thing.thing_status == 'Lent' && thing.owner == viewedUserProfile){
            badge_cont.setAttribute('class', 'badge-ribbon ribbon-lent')
            badge_cont.innerHTML = '<span class="badge-text ribbon-lent">LENT</span>';
        }else if(thing.thing_status == 'Lent' && thing.owner != viewedUserProfile){
            badge_cont.setAttribute('class', 'badge-ribbon ribbon-borrowed')
            badge_cont.innerHTML = '<span class="badge-text ribbon-borrowed">BORROWED</span>';
        }else if(thing.thing_status == 'Warehouse'){
            badge_cont.setAttribute('class', 'badge-ribbon ribbon-wh')
            badge_cont.innerHTML = '<span class="badge-text ribbon-wh">WAREHOUSE</span>';
        }
        
        container.append(badge_cont);

    // then disable LEND button
        const objButton = document.querySelector(`#lend-button-${thing.pk}`);
        objButton.innerText = 'CURRENTLY NOT ON KEEP';
        objButton.disabled = true;

    // then change disabled button color 
        const objButtonStyle = document.querySelector(`#lend-button-${thing.pk}-container`);
        objButtonStyle.className = 'form-submit-disabled flex_end_button';
    
    // then add the text that says its already been borrowed /LENT
        const objButtonMain = document.querySelector(`#objButtonFor-${thing.pk}`);
        const make_ObjStatusInfo = document.createElement('span');
        make_ObjStatusInfo.setAttribute('class', 'obj-title');
        make_ObjStatusInfo.setAttribute('id', `statusINFO-${thing.pk}`);
        make_ObjStatusInfo.innerHTML = `Borrowed by: <br>
                                        <a href="/u/${thing.current_borrower}">
                                                    ${thing.current_borrower}</a> <br>
                                        Return Due: <br><a href="#">
                                                    ${thing.promised_return}</a>`;
        objButtonMain.append(make_ObjStatusInfo)
}



function createBadge_Borrowed(thing, container) {
    //ADD BADGE: Borrowed
        const badge_cont = document.createElement('div');
        badge_cont.setAttribute('id', `badgeFor-${thing.pk}`);

        const viewedUserProfile = document.querySelector('#currentUser').innerText;
        const loggedUser = document.querySelector('#requestUser').innerText;

        if(thing.borrowed == true && thing.owner != viewedUserProfile){
            badge_cont.setAttribute('class', 'badge-ribbon ribbon-borrowed')
            badge_cont.innerHTML = '<span class="badge-text">BORROWED</span>';
        }else if(thing.borrowed == true && thing.owner == viewedUserProfile){
            badge_cont.setAttribute('class', 'badge-ribbon ribbon-lent')
            badge_cont.innerHTML = '<span class="badge-text">LENT</span>';
        }else if(thing.thing_status == 'Warehouse'){
            badge_cont.setAttribute('class', 'badge-ribbon ribbon-wh')
            badge_cont.innerHTML = '<span class="badge-text">WAREHOUSE</span>';
        }
        
        container.append(badge_cont);


    // making status when return pending
    const returnButton = document.querySelector(`#request-${thing.pk}-return`);
    const returnButtonContainer = document.querySelector(`#borrow-button-${thing.pk}-container`);

    if(thing.attempt_return && returnButton && returnButtonContainer){                
        returnButton.innerText = 'Return Pending...';
        returnButton.disabled = true;        
        returnButtonContainer.setAttribute('class', 'form-submit-disabled flex_end_button')
    }


    // then add the text that says its already been borrowed /LENT
    const objButtonMain = document.querySelector(`#objButtonFor-${thing.pk}`);
    const make_ObjStatusInfo = document.createElement('span');
    
    if(thing.borrowed == true && thing.owner != viewedUserProfile && loggedUser == thing.current_borrower){
        make_ObjStatusInfo.setAttribute('class', 'obj-title');
        make_ObjStatusInfo.setAttribute('id', `statusINFO-${thing.pk}`);
        make_ObjStatusInfo.innerHTML = `You Borrowed this from: <br>
                                        <a href="/u/${thing.owner}">
                                                    ${thing.owner}</a> <br>
                                        Return this at or before: <br><a href="#">
                                                    ${thing.promised_return}</a>`;
        objButtonMain.append(make_ObjStatusInfo)
        
    }else if(thing.borrowed == true && thing.owner == viewedUserProfile && viewedUserProfile == loggedUser){
        make_ObjStatusInfo.setAttribute('class', 'obj-title');
        make_ObjStatusInfo.setAttribute('id', `statusINFO-${thing.pk}`);
        make_ObjStatusInfo.innerHTML = `Borrowed by: <br>
                                        <a href="/u/${thing.current_borrower}">
                                                    ${thing.current_borrower}</a> <br>
                                        Return Due: <br><a href="#">
                                                    ${thing.promised_return}</a>`;
        objButtonMain.append(make_ObjStatusInfo)

        // then disable BORROWED button
        const objButton = document.querySelector(`#borrow-button-${thing.pk}`);
        
        objButton.innerText = 'CURRENTLY NOT ON KEEP';
        objButton.disabled = true;
    
        // then change disabled button color 
            const objButtonStyle = document.querySelector(`#borrow-button-${thing.pk}-container`);
            objButtonStyle.className = 'form-submit-disabled flex_end_button';
    }else if(thing.borrowed == true && thing.owner == viewedUserProfile && viewedUserProfile != loggedUser){
        make_ObjStatusInfo.setAttribute('class', 'obj-title');
        make_ObjStatusInfo.setAttribute('id', `statusINFO-${thing.pk}`);
        make_ObjStatusInfo.innerHTML = `You Borrowed this!!!<br>
                                        Return Due: <br><a href="#">
                                                    ${thing.promised_return}</a>`;
        objButtonMain.append(make_ObjStatusInfo)

    }
    
        
        
}












function createConatentTitle(thing, container) {
    // CC-TITLE
    const create_thingTitle = document.createElement('div');
    create_thingTitle.setAttribute('class', 'cc-title');
    create_thingTitle.setAttribute('id', `thing-${thing.pk}-title`);
    container.append(create_thingTitle);
        // THE TITLE
        const thingTitle = document.querySelector(`#thing-${thing.pk}-title`);
        thingTitle.innerHTML = `<span class="obj-title">&nbsp;${thing.thing_name}</span>`;
    
    // CC-PICTURE
    const create_thingPIC = document.createElement('div');
    create_thingPIC.setAttribute('class', 'cc-picture');
    create_thingPIC.setAttribute('id', `thing-${thing.pk}-pic`);
    container.append(create_thingPIC);
        // THE PIC
        const thingPic =  document.querySelector(`#thing-${thing.pk}-pic`);
        
        thingPic.innerHTML = `<img src="${thing.thing_thumbnail}" alt="${thing.thing_name}">`;          
    
    // CC-DETAILS
    const create_thingDetails = document.createElement('div');
    create_thingDetails.setAttribute('class', 'cc-details');
    create_thingDetails.setAttribute('id', `thing-${thing.pk}-details`);
    container.append(create_thingDetails);

    const thingDetails = document.querySelector(`#thing-${thing.pk}-details`);

        // CC-ID-CONTAINER ------------------------------------------------
        const create_thingCCID = document.createElement('div');
        create_thingCCID.setAttribute('class', 'ccdet-item');
        create_thingCCID.setAttribute('id', `thing-${thing.pk}-item-ID`);
        thingDetails.append(create_thingCCID);

        const thingCCID = document.querySelector(`#thing-${thing.pk}-item-ID`);

            // CC-ID
            const thingCCID_makeTitle = document.createElement('div');
            thingCCID_makeTitle.setAttribute('class', 'ccdet-title');
            thingCCID_makeTitle.innerHTML = '<span>ID:&nbsp;</span>'
            thingCCID.append(thingCCID_makeTitle);

            // ITEM-ID
            const thingCCID_item = document.createElement('div');
            thingCCID_item.setAttribute('class', 'ccdet-info');
            thingCCID_item.innerHTML = `<span>&nbsp;${thing.pk}</span>`;
            thingCCID.append(thingCCID_item);


        // CC-SN-CONTAINER ------------------------------------------------
        const create_thingCCSN = document.createElement('div');
        create_thingCCSN.setAttribute('class', 'ccdet-item');
        create_thingCCSN.setAttribute('id', `thing-${thing.pk}-item-SN`);
        thingDetails.append(create_thingCCSN);

        const thingCCSN = document.querySelector(`#thing-${thing.pk}-item-SN`);

            // CC-SN
            const thingCCSN_makeTitle = document.createElement('div');
            thingCCSN_makeTitle.setAttribute('class', 'ccdet-title');
            thingCCSN_makeTitle.innerHTML = '<span>SN:&nbsp;</span>';
            thingCCSN.append(thingCCSN_makeTitle);

            // ITEM-SN
            const thingCCSN_item = document.createElement('div');
            thingCCSN_item.setAttribute('class', 'ccdet-info');
            thingCCSN_item.innerHTML = `<span>&nbsp;${thing.thing_sn}</span>`;
            thingCCSN.append(thingCCSN_item);

        // CC-ADDED-CONTAINER ------------------------------------------------
        const create_thingCCADDED = document.createElement('div');
        create_thingCCADDED.setAttribute('class', 'ccdet-item');
        create_thingCCADDED.setAttribute('id', `thing-${thing.pk}-item-ADDED`);
        thingDetails.append(create_thingCCADDED);

        const thingCCADDED = document.querySelector(`#thing-${thing.pk}-item-ADDED`);

            // CC-SN
            const thingCCADDED_makeTitle = document.createElement('div');
            thingCCADDED_makeTitle.setAttribute('class', 'ccdet-title');
            thingCCADDED_makeTitle.innerHTML = '<span>ADDED:&nbsp;</span>';
            thingCCADDED.append(thingCCADDED_makeTitle);

            // ITEM-SN
            const thingCCADDED_item = document.createElement('div');
            thingCCADDED_item.setAttribute('class', 'ccdet-info');
            thingCCADDED_item.innerHTML = `<span>&nbsp;${thing.date_added}</span>`;
            thingCCADDED.append(thingCCADDED_item);

        // CC-CONDITION-CONTAINER ------------------------------------------------
        const create_thingCCCONDITION = document.createElement('div');
        create_thingCCCONDITION.setAttribute('class', 'ccdet-item');
        create_thingCCCONDITION.setAttribute('id', `thing-${thing.pk}-item-CONDITION`)
        thingDetails.append(create_thingCCCONDITION);

        const thingCCCONDITION = document.querySelector(`#thing-${thing.pk}-item-CONDITION`);

            // CC-CONDITION
            const thingCCCONDITION_makeTitle = document.createElement('div');
            thingCCCONDITION_makeTitle.setAttribute('class', 'ccdet-title');
            thingCCCONDITION_makeTitle.innerHTML = '<span>CONDITION:&nbsp;</span>';
            thingCCCONDITION.append(thingCCCONDITION_makeTitle);

            // ITEM-STATUS
            const thingCCCONDITION_item = document.createElement('div');
            thingCCCONDITION_item.setAttribute('class', 'ccdet-info');
            thingCCCONDITION_item.innerHTML = `<span>&nbsp;${thing.thing_condition}</span>`;
            thingCCCONDITION.append(thingCCCONDITION_item);
}






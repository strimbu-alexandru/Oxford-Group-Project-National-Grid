//Preventing redirects on form submittal
$(function() {
    $("#revokePass").on("submit", function(e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: 'get',
            data: $(this).serialize(),
            success: function(data) {
                $('#revokeSuccessAlert').show();
             }
        });
    });
});

$(function() {
    $("#edit").on("submit", function(e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: 'post',
            data: $(this).serialize(),
            success: function(data) {
                $('#editSuccessAlert').show();
             }
        });
    });
});

$(function() {
    $("#chargeSlotAdd").on("submit", function(e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: 'post',
            data: $(this).serialize(),
            success: function(data) {
                $('#slotSuccessAlert').show();
             }
        });
    });
});

$(function() {
    $("#mobileLogin").on("submit", function(e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: 'post',
            data: $(this).serialize(),
            success: function(data) {
                console.log(data);
                if(data == 'nosuchuser'){
                    $("#wrongPassAlert").show();
                 }
                else{
                    var signInButton = document.getElementById("signIn");
                    var loggedInElements = document.getElementsByClassName("view-loggedin");
                    var disabledElements = document.getElementsByClassName("disabled-logout");
                    signInButton.style.display="none";
                    for(var i = 0; i < loggedInElements.length; i++){
                        loggedInElements[i].style.display="block";

                }
                for(var i = 0; i < disabledElements.length; i++){
                    disabledElements[i].disabled=false;
                }
                $("#loginModal").modal('hide');
             }
         }
        });
    });
});

$(function(){
    $('#loginModal').on('hide.bs.modal', function (e) {
     $('#wrongPassAlert').hide();
    });
});


$(function() {
    $("#deleteAllDevices").on("submit", function(e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: 'get',
            data: $(this).serialize(),
            success: function(data) {
                $('#deleteAllAlert').show();
                var el = document.getElementById('deviceList');

                var xhr = new XMLHttpRequest();
                xhr.open('GET', 'userDevices/get', true);
                xhr.onload = function() {
                deviceList = JSON.parse(xhr.response);
                while (el.firstChild) {
                    el.removeChild(el.firstChild);
                }
                if(deviceList.length > 0){
                //Reset the form


                for(var i = 0; i<deviceList.length; i++){
                    var node = document.createElement('li');
                    node.className = "list-group-item";
                    node.innerHTML = deviceList[i].deviceName +'<i class="js-remove">✖</i>';
                    node.value = i;
                    el.appendChild(node);
                }
            }
            else
            {
                var textContent = document.createTextNode("No devices currently registered!");
                el.appendChild(textContent);
            }
            };
            xhr.send();

             }
        });
    });
});

$(function() {
    $("#deleteAllSlotDevices").on("submit", function(e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: 'get',
            data: $(this).serialize(),
            success: function(data) {
                showSlotList();
             }
        });
    });
});
//Hides alerts when modal is closed
$(function(){
    $('#managePassModal').on('hide.bs.modal', function (e) {
     $('#revokeSuccessAlert').hide();
     $('#editSuccessAlert').hide();
    });
});

$(function(){
    $('#manageModal').on('hide.bs.modal', function (e) {
     $('#deleteAllAlert').hide();
    });
});

$(function(){
    $('#resultsModal').on('hide.bs.modal', function (e) {
     $('#registerSuccessAlert').hide();
     $('#registerSlotAlert').hide();
     $('#registeredUsedAlert').hide();
     $('#doubleClickAlert').hide();
    });
});

//Reusable alerts
$(function(){
    $("[data-hide]").on("click", function(){
        $("." + $(this).attr("data-hide")).hide();
        // -or-, see below
        // $(this).closest("." + $(this).attr("data-hide")).hide();
    });
});


var options =[{"text"  : "iPhone","deviceName" : "iPhone", "consumption": "0.012", "timeToCharge": "100"},
    {"text"     : "Android","deviceName"    : "Android",	"consumption":"0.015", "timeToCharge":"90"},
    {"text"     : "Tesla",  "deviceName"    : "Tesla",     "consumption":"120",   "timeToCharge":"75"},
    {"text"     : "Wahing machine", "deviceName" : "Washing machine", "consumption": "0.5", "timeToCharge" : "100"},
    {"text"     : "Custom", "deviceName" : "Custom",       "consumption":"0", "timeToCharge":"0"}
    ];


function formsubmit(id, p=0, m=0, toDB = false){

    switch(id){
        case "template":
            $("#registerSuccessAlert").hide();
            $("#registerUsedAlert").hide();
            var vals = $('#templateDevices').val() || [];
            var listDevs = [];

            var p = options[vals[0]].consumption;
            var m = options[vals[0]].timeToCharge;
            var radios = document.getElementsByName('periodTemplate');
            
            var api = ""

				for (var i = 0, length = radios.length; i < length; i++)
				{
 					if (radios[i].checked)
 					{
  						api = radios[i].value
  						break;
 					}
				}
                $.ajax('./server/' + api + '/'+p+'/'+m, {
                success: function(data) {
                //listDevs.push({'data': data, 'm':m});
                writeschedule(options[vals[0]], data, m);
            }
            }
            );
            break;

        case "owndevice":
            $("#registerSuccessAlert").hide();
            $("#registerUsedAlert").hide();
            var radios = document.getElementsByName('periodOwn');
            
            var api = ""

				for (var i = 0, length = radios.length; i < length; i++)
				{
 					if (radios[i].checked)
 					{
  						api = radios[i].value
  						break;
 					}
				}

                var vals = $.parseJSON($('#ownDevices option:selected').val());

                var p = vals.consumption;
                var m = vals.timeToCharge;
                $.ajax('./server/' + api + '/'+p+'/'+m, {
                success: function(data) {
                writeschedule(vals, data, m);
            }
            }
            );
            break;

        case "newdevice":
                $("#registerSuccessAlert").hide();
				$("#registerUsedAlert").hide();
				var radios = document.getElementsByName('periodNew');
            
                var api = "";

				for (var i = 0, length = radios.length; i < length; i++)
				{
 					if (radios[i].checked)
 					{
  						api = radios[i].value
  						break;
 					}
				}

                if(toDB){
            	$("#registerUsedAlert").show();
                $("#custdata").submit(function(e) {

                $.ajax({
                    type: "POST",
                    url: "userDevices/add",
                    data: $("#custdata").serialize(), // serializes the form's elements.
                    success: function(data)
                    {
                        if(data == "success")			//different messages for success or name already in use
                            {$("#registerUsedAlert").hide(); $("#registerSuccessAlert").show()}
                    }
                    });

                 e.preventDefault(); // avoid to execute the actual submit of the form.
                });

                $("#custdata").submit();
            }


            $.ajax('./server/' + api + '/'+p+'/'+m, {
            success: function(data) {
                var deviceObject = $('#custdata').serializeArray().reduce(function(a, x) { a[x.name] = x.value; return a; }, {});

                writeschedule(deviceObject, data, m);
            }
            });
            break;
    }

    Chart.pluginService.register({
    beforeDraw: function (chart) {
        if (chart.config.options.elements.center) {
    //Get ctx from string
    var ctx = chart.chart.ctx;

            //Get options from the center object in options
    var centerConfig = chart.config.options.elements.center;
    var fontStyle = centerConfig.fontStyle || 'Arial';
    var texts = centerConfig.texts;
    var color = centerConfig.color || '#000';
    var sidePadding = centerConfig.sidePadding || 20;
    var sidePaddingCalculated = (sidePadding/100) * (chart.innerRadius * 2)
    //Start with a base font of 30px
    ctx.font = "30px " + fontStyle;

            //Get the width of the string and also the width of the element minus 10 to give it 5px side padding
    var stringWidth = 0;
    for(var i = 0; i<texts.length; i++)
    {
        if(ctx.measureText(texts[i]).width > stringWidth)
            stringWidth = ctx.measureText(texts[i]).width;
    }
    var elementWidth = (chart.innerRadius * 2) - sidePaddingCalculated;

    // Find out how much the font can grow in width.
    var widthRatio = elementWidth / stringWidth;
    var newFontSize = Math.floor(30 * widthRatio);
    var elementHeight = (chart.innerRadius * 2);

    // Pick a new font size so it will not be larger than the height of label.
    var fontSizeToUse = Math.min(newFontSize, elementHeight);

            //Set font settings to draw it correctly.
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    var centerX = ((chart.chartArea.left + chart.chartArea.right) / 2);
    var centerY = ((chart.chartArea.top + chart.chartArea.bottom) / 2);
    ctx.font = fontSizeToUse+"px " + fontStyle;
    ctx.fillStyle = color;

    //Draw text in center
    for(var i = 0; i< texts.length; i++){
        ctx.fillText(texts[i], centerX, centerY + (i  - (texts.length-1)/2)*fontSizeToUse);
    }
        }
    }
});
}

function setCharAt(str,index,chr) {
    if(index > str.length-1) return str;
    return str.substr(0,index) + chr + str.substr(index+1);
}

function writeschedule(device, data, m){
    //Calculate length of single charge
    var hours = m/60;
    var plugDate =data.data[0].plugInTime;
    var carbProd = data.data[0].carbonProduced;
    var carbSaved = data.data[0].carbonReduced;
    carbProd = Math.round(carbProd * 100) / 100;
    var energy = data.data[0].energyConsumed;
    energy = Math.round(energy * 100) / 100;
    plugDate = plugDate.split("T").pop();
    plugDate = plugDate.substring(0,plugDate.length-1);
    var plugDateShort = plugDate.split(":")[0];
    var plugDateMins = plugDate.split(":")[1];
    var plugDateTime = data.data[0].plugInTime;
    plugDateTime = setCharAt(plugDateTime,10,' ');
    plugDateTime = setCharAt(plugDateTime,16,' ');

    var unplugShort = plugDateShort*1 + hours*1 + (1*plugDateMins)/60;

    var numberCharging = [];
    var backgroundColors = [];

    //fakes numberCharging, I hope to get this from db
    for(var i = 0; i<24; i++){
            if(unplugShort <= 24){
                if(i >= plugDateShort && i < unplugShort)
                numberCharging.push(1);
            else
                numberCharging.push(0);
            }
            else{
                if(i >= plugDateShort || i < unplugShort-24)
                    numberCharging.push(1);
                else
                numberCharging.push(0);
            }                
            
        }

        for(var i = 0; i<24; i++){
            if(numberCharging[i]<1)
                backgroundColors.push('LightGray');
            else
                backgroundColors.push('ForestGreen');
        }
    $('#readyToWrite').attr("value", true);
    $('#inputSlotName').attr("value", device.deviceName);
    $('#inputSlotPower').attr("value", device.consumption);
    $('#inputSlotMinutes').attr("value" ,m);
    $('#deviceSlotId').attr("value", device.deviceId);
    $('#inputSlotPlugIn').attr("value", plugDateTime.substring(0, 16));

    $('#resultsModal').modal('show');

    var ctx = document.getElementById('schedulerchart');
        var schChart = new Chart(ctx,{
            type: 'doughnut',
            data: {
                labels: ['00:00','01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','10:00','11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
                datasets: [{
                    label: '',
                    data: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    backgroundColor: backgroundColors,
                    hoverBackgroundColor: backgroundColors,
                },
                    {
                    label: '',
                    data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    backgroundColor: backgroundColors,
                    hoverBackgroundColor: backgroundColors,
                }
                ]
            },
            options: {
                tooltips: {
                    callbacks: {
                            title: function(tooltipItem, data){
                                return data['labels'][tooltipItem[0]['index']];
                            },
                            label: function(tooltipItem, data){
                            },
                            afterLabel: function(tooltipItem, data){
                                var texts = [];
                                var number = numberCharging[tooltipItem.index];
                                var text;
                                if(number == 1)
                                    text = ' device charging at this time.';
                                else
                                    text = ' devices charging at this time.';
                                text = number + text;
                                texts.push(text);
                                if(tooltipItem.index == plugDateShort){
                                    text = "Plug in your device at " + plugDate + ".";
                                    texts.push(text);
                                }
                                return texts;
                            }
                    }
                },
                elements: {
                    center: {
                        texts: ["You should plug in at ",
                                plugDateTime,
                                "to use only " + Math.round(carbProd * energy * 100) / 100 + " g of carbon.",
                                "You save " + Math.round(carbSaved * 100)/100 + " g by waiting."
                                ],
                        fontStyle: 'Helvetica', // Default is Arial
                         sidePadding: 10 // Defualt is 20 (as a percentage)
                }
            },
                legend:{
                    display: false
                },
                layout: {
                    padding: {
                        left: 0,
                        right: 0,
                        top: 15,
                        bottom: 0
                    }
                },
                responsive: true,
                maintainAspectRatio: false,
                cutoutPercentage: 75
            }
        });

}


function onSignIn(googleUser) {
                var loginHandler = 'auth/login';

    var profile = googleUser.getBasicProfile();
    var signInButton = document.getElementById("signIn");
    var loggedInElements = document.getElementsByClassName("view-loggedin");
    var disabledElements = document.getElementsByClassName("disabled-logout");
    signInButton.style.display="none";
    for(var i = 0; i < loggedInElements.length; i++){
        loggedInElements[i].style.display="block";
    }

    for(var i = 0; i < disabledElements.length; i++){
        disabledElements[i].disabled=false;
    }

    var id_token = googleUser.getAuthResponse().id_token;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', loginHandler, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        jwToken = xhr.responseText;
    };
    xhr.send('idtoken=' + id_token);
}

function signOut() {

    var logoutHandler = 'auth/logout'

    var auth2 = gapi.auth2.getAuthInstance();
                auth2.signOut().then(function () {
                });
    var signInButton = document.getElementById("signIn");
    var loggedInElements = document.getElementsByClassName("view-loggedin");
    var disabledElements = document.getElementsByClassName("disabled-logout");
    signInButton.style.display="block";
    for(var i = 0; i < loggedInElements.length; i++){
        loggedInElements[i].style.display="none";
    }

    for(var i = 0; i < disabledElements.length; i++){
        disabledElements[i].disabled=true;
    }

    // tell server to sign user out
    var xhr = new XMLHttpRequest();
    xhr.open('GET', logoutHandler);
    xhr.onload = function() {
      jwToken='';
    };
    xhr.send();
}

function showPassManager(){
    $('#managePassModal').modal('show');
}

function showElList(){
    var el = document.getElementById('deviceList');
    var deviceGet = 'userDevices/get';

    var deviceList = [];

    var xhr = new XMLHttpRequest();
    xhr.open('GET', deviceGet, true);
    xhr.onload = function() {
        deviceList = JSON.parse(xhr.response);
        while (el.firstChild) {
                el.removeChild(el.firstChild);
            }
        if(deviceList.length > 0){
            //Reset the form

            for(var i = 0; i<deviceList.length; i++){
                var node = document.createElement('li');
                node.className = "list-group-item";
                node.innerHTML = deviceList[i].deviceName +'<i class="js-remove">✖</i>';
                node.value = deviceList[i].deviceName;
                el.appendChild(node);
            }
        }
        else
        {
            var textContent = document.createTextNode("No devices currently registered!");
            el.appendChild(textContent);
        }
    };
    xhr.send();

    // Editable list
    var editableList = Sortable.create(el, {
    filter: '.js-remove',
    onFilter: function (evt) {
        var dragged = editableList.closest(evt.item); // get dragged item
        var deviceDelete = 'userDevices/delete';

        var xhr = new XMLHttpRequest();
        xhr.open('GET', deviceDelete + '/'+ dragged.innerHTML.split('<', 1)[0], true);
        xhr.onload = function() {
        };

        xhr.send();

        dragged && dragged.parentNode.removeChild(dragged);
        event.stopPropagation()
        evt.preventDefault();
    }
    });

    $('#manageModal').modal('show');

}


function loadOwnDevices(){
    var deviceGet = 'userDevices/get';
    var deviceList = [];
    var el = document.getElementById('ownDevices');

    var xhr = new XMLHttpRequest();
    xhr.open('GET', deviceGet, true);
    xhr.onload = function() {
        deviceList = JSON.parse(xhr.response);
    //Clear form
    while (el.firstChild) {
    el.removeChild(el.firstChild);}

        //Populate the form with values
        for(var i = 0; i<deviceList.length; i++)
        {
            var node = document.createElement('option');
            node.value = '{"id":' + i + ', "deviceName": "'+ deviceList[i].deviceName +'", "deviceId": '+ deviceList[i].deviceId + ', "consumption":' + deviceList[i].consumption + ', "timeToCharge":' + deviceList[i].timeToCharge + '}';
            node.innerHTML = deviceList[i].deviceName;

            el.appendChild(node);
        }
    };
    xhr.send();

}

//Showing collapsible sidebar
$(function () {
  'use strict'

  $('[data-toggle="offcanvas"]').on('click', function () {
    $('.offcanvas-collapse').toggleClass('open')
  })
})

function mobileSignOut() {

    var logoutHandler = 'auth/logout'

    var signInButton = document.getElementById("signIn");
    var loggedInElements = document.getElementsByClassName("view-loggedin");
    var disabledElements = document.getElementsByClassName("disabled-logout");
    signInButton.style.display="block";
    for(var i = 0; i < loggedInElements.length; i++){
        loggedInElements[i].style.display="none";
    }

    for(var i = 0; i < disabledElements.length; i++){
        disabledElements[i].disabled=true;
    }

    // tell server to sign user out
    var xhr = new XMLHttpRequest();
    xhr.open('GET', logoutHandler);
    xhr.onload = function() {
      jwToken='';
    };
    xhr.send();
}

function showSlotList(){
    var el = document.getElementById("slotList");
    var deviceGet = 'chargingSlots/get/true';

    var deviceList = [];

    $("#chargeManageModal").modal("show");

    var xhr = new XMLHttpRequest();
    xhr.open('GET', deviceGet, true);
    xhr.onload = function() {
        deviceList = JSON.parse(xhr.response);

        chargeSlotsVisualiser(deviceList);
        while (el.firstChild) {
                el.removeChild(el.firstChild);
            }
        if(deviceList.length > 0){

            for(var i = 0; i<deviceList.length; i++){
                var node = document.createElement('li');
                node.className = "list-group-item";
                node.innerHTML = deviceList[i].deviceName + '<i class="js-remove">✖</i>';
                node.value = deviceList[i].slotId;
                el.appendChild(node);
            }
        }
        else
        {
            var textContent = document.createTextNode("No devices currently registered!");
            el.appendChild(textContent);
        }
    };
    xhr.send();

    // Editable list
    var editableList = Sortable.create(el, {
    filter: '.js-remove',
    onFilter: function (evt) {
        var dragged = editableList.closest(evt.item); // get dragged item
        var deviceDelete = 'chargingSlots/delete';

        var xhr = new XMLHttpRequest();
        xhr.open('GET', deviceDelete + '/'+ dragged.value, true);
        xhr.onload = function() {
        };

        xhr.send();
        if(dragged.parentNode)
            dragged && dragged.parentNode.removeChild(dragged);
        showSlotList();
        event.stopPropagation();
        evt.preventDefault();
    }
    });

    //Register chart?
    Chart.pluginService.register({
    beforeDraw: function (chart) {
        if (chart.config.options.elements.center) {
    //Get ctx from string
    var ctx = chart.chart.ctx;

            //Get options from the center object in options
    var centerConfig = chart.config.options.elements.center;
    var fontStyle = centerConfig.fontStyle || 'Arial';
    var texts = centerConfig.texts;
    var color = centerConfig.color || '#000';
    var sidePadding = centerConfig.sidePadding || 20;
    var sidePaddingCalculated = (sidePadding/100) * (chart.innerRadius * 2)
    //Start with a base font of 30px
    ctx.font = "30px " + fontStyle;

            //Get the width of the string and also the width of the element minus 10 to give it 5px side padding
    var stringWidth = 0;
    for(var i = 0; i<texts.length; i++)
    {
        if(ctx.measureText(texts[i]).width > stringWidth)
            stringWidth = ctx.measureText(texts[i]).width;
    }
    var elementWidth = (chart.innerRadius * 2) - sidePaddingCalculated;

    // Find out how much the font can grow in width.
    var widthRatio = elementWidth / stringWidth;
    var newFontSize = Math.floor(30 * widthRatio);
    var elementHeight = (chart.innerRadius * 2);

    // Pick a new font size so it will not be larger than the height of label.
    var fontSizeToUse = Math.min(newFontSize, elementHeight);

            //Set font settings to draw it correctly.
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    var centerX = ((chart.chartArea.left + chart.chartArea.right) / 2);
    var centerY = ((chart.chartArea.top + chart.chartArea.bottom) / 2);
    ctx.font = fontSizeToUse+"px " + fontStyle;
    ctx.fillStyle = color;

    //Draw text in center
    for(var i = 0; i< texts.length; i++){
        ctx.fillText(texts[i], centerX, centerY + (i  - (texts.length-1)/2)*fontSizeToUse);
    }
        }
    }
});


}

function chargeSlotsVisualiser(deviceList){
    var numberCharging = [];
    var backgroundColors = [];
    var deviceNames = [];

    for(var i = 0; i<24; i++){
        var count = 0;
        deviceNames.push([]);
        for(var j = 0; j<deviceList.length; j++){
            var plugDate = deviceList[j].plugInTime;
            plugDate = plugDate.split(" ").pop();
            plugDate = plugDate.substring(0,plugDate.length-1);
            var plugDateShort = plugDate.split(":")[0];
            var unplugShort = 1*plugDateShort + deviceList[j].timeToCharge/60;
            if(unplugShort <= 24){
                if(i >= plugDateShort && i < unplugShort)
                {
                count=count + 1;
                deviceNames[i].push(deviceList[j].deviceName);
                }
            }
            else{
                if(i >= plugDateShort || i < unplugShort-24){
                    count = count + 1;
                    deviceNames[i].push(deviceList[j].deviceName);
                }
            }

            
        }
        numberCharging.push(count);
    }


    for(var i = 0; i<24; i++){
        switch(numberCharging[i]){
            case 0: backgroundColors.push('LightGray'); break;
            case 1: backgroundColors.push('MediumSeaGreen'); break;
            case 2: backgroundColors.push('ForestGreen'); break;
            default: backgroundColors.push('DarkGreen'); break;
        }
    }


    var ctx1 = document.getElementById('slotchart');

    var schChart = new Chart(ctx1,{
        type: 'doughnut',
        data: {
            labels: ['00:00','01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','10:00','11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
            datasets: [{
                label: '',
                data: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                backgroundColor: backgroundColors,
                hoverBackgroundColor: backgroundColors},
                {
                label: '',
                    data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    backgroundColor: backgroundColors,
                    hoverBackgroundColor: backgroundColors,}
                ]
            },
            options: {
                tooltips: {
                    callbacks: {
                            title: function(tooltipItem, data){
                                return data['labels'][tooltipItem[0]['index']];
                            },
                            label: function(tooltipItem, data){},
                            afterLabel: function(tooltipItem, data){
                                var labeltext = [];
                                var number = numberCharging[tooltipItem.index];
                                var text;
                                if(number == 1)
                                    text = ' device charging at this time';
                                else
                                    text = ' devices charging at this time';
                                labeltext.push(number + text);
                                for(var i = 0; i<deviceNames[tooltipItem.index].length; i++){
                                    labeltext.push(deviceNames[tooltipItem.index][i]);
                                }
                                return labeltext;
                            },
                    }
                },
                elements: {
                    center: {
                        texts: ["You have " + deviceList.length + " devices scheduled",
                                "for the next 24 hours.",
                                "Hover to see exact plugin times."
                                ],
                        fontStyle: 'Helvetica', // Default is Arial
                         sidePadding: 10 // Defualt is 20 (as a percentage)
                }
            },
                legend:{
                    display: false
                },
                layout: {
                    padding: {
                        left: 0,
                        right: 0,
                        top: 15,
                        bottom: 0
                    }
                },
                responsive: true,
                maintainAspectRatio: false,
                cutoutPercentage: 75
            }
        });
}

function addSlot(){
    if($('#readyToWrite').val()){
        $("#hiddenForm").off();
        $("#hiddenForm").submit(function(e) {
                    $.ajax({
                            type: "POST",
                            url: "chargingSlots/add",
                            data: $("#hiddenForm").serialize(), // serializes the form's elements.
                            beforeSend: function(){
                                document.getElementById('addButton').disabled=true;
                                window.setTimeout(function(){}, 10);
                            },
                            success: function(data)
                            { 
                                if(data == "success")           //different messages for success or name already in use
                                    {$("#registerSlotAlert").show();
                                    $('#readyToWrite').attr("value", null);}
                                    document.getElementById('addButton').disabled=false;
                            }
                            });
                         
                         e.stopPropagation();
                         e.preventDefault(); // avoid to execute the actual submit of the form.
                        });

            $("#hiddenForm").submit();

    }
    else{
        $('#doubleClickAlert').show();
    }
}
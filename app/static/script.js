var options =[{"text"  : "iPhone","value" : "iPhone", "power": "30", "minutes": "120"},
    {"text"     : "Android","value"    : "Android",	"power":"70", "minutes":"300"},
    {"text"  : "Custom","value" : "Custom", "power":"0", "minutes":"0"}
    ];


function formsubmit(id, p=0, m=0, toDB = false){

    switch(id){
        case "template":
            var vals = $('#templateDevices').val() || [];
            var listDevs = [];

            var p = options[vals[0]].power;
            var m = options[vals[0]].minutes;
                $.ajax('./server/best24h/'+p+'/'+m, {
                success: function(data) {
                //listDevs.push({'data': data, 'm':m});
                writeschedule(data, m); 
            }
            }
            );
            break;

        case "owndevice":
            var vals = $('ownDevices').val();
            var listDevs = [];
            for(var i =0; i<vals.length; i++)
            {
                var p = vals[i].value.power;
                var m = vals[i].value.minutes;
                $.ajax('./server/best24h/'+p+'/'+m, {
                success: function(data) {
                listDevs.push({'data': data, 'm':m});
                
            }
            }
            );
            }
            writeschedule(listDevs);
            break;

        case "newdevice":
            var form = document.getElementById('custdata');
            if(toDB){
                form.submit();
            }


            $.ajax('./server/best24h/'+p+'/'+m, {
            success: function(data) {
                //var listDevs = [{'data': data, 'm':m}];
                writeschedule(data,m);
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
            var txt1 = centerConfig.text1;
            var txt2 = centerConfig.text2;
    var color = centerConfig.color || '#000';
    var sidePadding = centerConfig.sidePadding || 20;
    var sidePaddingCalculated = (sidePadding/100) * (chart.innerRadius * 2)
    //Start with a base font of 30px
    ctx.font = "30px " + fontStyle;
    
            //Get the width of the string and also the width of the element minus 10 to give it 5px side padding
    var stringWidth = ctx.measureText(txt1).width;
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
    ctx.fillText(txt1, centerX, centerY-0.8*fontSizeToUse);
    ctx.fillText(txt2, centerX, centerY+0.8*fontSizeToUse);
        }
    }
});
}

function setCharAt(str,index,chr) {
    if(index > str.length-1) return str;
    return str.substr(0,index) + chr + str.substr(index+1);
}

function writeschedule(data, m){
    //Calculate length of single charge
    var hours = m/60;var mins = m%60;
    var plugDate =data.data[2].plugInTime;
    plugDate = plugDate.split("T").pop();
    plugDate = plugDate.substring(0,plugDate.length-1);
    var plugDateShort = plugDate.split(":")[0];
    var plugDateMins = plugDate.split(":")[1];
    var plugDateTime = data.data[2].plugInTime;
    plugDateTime = setCharAt(plugDateTime,10,' ');
    plugDateTime = setCharAt(plugDateTime,16,' ');

    var unplugShort = plugDateShort*1 + hours*1 + (1*plugDateMins + 1*mins)/60;

    var numberCharging = [];
    var backgroundColors = [];

    //fakes numberCharging, I hope to get this from db
    for(var i = 0; i<24; i++){
            if(i >= plugDateShort && i <= unplugShort)
                numberCharging.push(1);
            else
                numberCharging.push(0);
        }

        for(var i = 0; i<24; i++){
            if(numberCharging[i]<1)
                backgroundColors.push('gray');
            else
                backgroundColors.push('green');
        }



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
                },
                    {
                    label: '',
                    data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    backgroundColor: backgroundColors,
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
                                var number = numberCharging[tooltipItem.index];
                                var text;
                                if(number == 1)
                                    text = ' device charging at this time.';
                                else
                                    text = ' devices charging at this time.';
                                return number + text;
                            },
                            afterLabel: function(tooltipItem, data){
                                var text = '';
                                if(tooltipItem.index == plugDateShort){
                                    text = "Plug in your device at ";
                                    text = text + plugDate + ".";
                                }
                                return text;
                            }
                    }
                },
                elements: {
                    center: {
                        text1: "You should plug in at ",
                        text2: plugDateTime,
                        fontStyle: 'Helvetica', // Default is Arial
                         sidePadding: 20 // Defualt is 20 (as a percentage)
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
                var loginHandler = 'http://team10.pythonanywhere.com/auth/login';

    var profile = googleUser.getBasicProfile();
    var signInButton = document.getElementById("signIn");
    var signOutText = document.getElementById("signOut");
    var manageLink = document.getElementById("manage");

    signInButton.style.display="none";
    signOutText.style.display="block";
    manageLink.style.display="block";
    
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.

    var id_token = googleUser.getAuthResponse().id_token;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', loginHandler, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        console.log(xhr.responseText);
        jwToken = xhr.responseText;
    };
    xhr.send('idtoken=' + id_token);
}

function signOut() {

    var logoutHandler = 'http://team10.pythonanywhere.com/auth/logout'

    var auth2 = gapi.auth2.getAuthInstance();
                auth2.signOut().then(function () {
                    console.log('User signed out.');
                });
    var signInButton = document.getElementById("signIn");
    var signOutText = document.getElementById("signOut");
    var manageLink = document.getElementById("manage");
    signInButton.style.display="block";
    signOutText.style.display="none";
    manageLink.style.display="none";

    // tell server to sign user out
    var xhr = new XMLHttpRequest();
    xhr.open('GET', logoutHandler);
    xhr.onload = function() {
      console.log(xhr.responseText);
      jwToken='';
    };
    xhr.send();
}


function showElList(){
    var el = document.getElementById('deviceList');
    var deviceGet = 'http://team10.pythonanywhere.com/userDevices/get';

    var deviceList = [];

    var xhr = new XMLHttpRequest();
    xhr.open('GET', deviceGet, true);
    xhr.onload = function() {
        deviceList = JSON.parse(xhr.response);

        if(deviceList.length > 0){
            //Reset the form
            while (el.firstChild) {
                el.removeChild(el.firstChild);
            }

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

    // Editable list
    var editableList = Sortable.create(el, {
    filter: '.js-remove',
    onFilter: function (evt) {
        var el = editableList.closest(evt.item); // get dragged item
        console.log(el);
        var deviceDelete = 'http://team10.pythonanywhere.com/userDevices/delete';

        var xhr = new XMLHttpRequest();
        xhr.open('GET', deviceDelete + '/'+ deviceList[el.value].deviceName, true);
        xhr.onload = function() {
        };

        xhr.send();
        el && el.parentNode.removeChild(el);
    }
    });

    $('#manageModal').modal('show');

}


function loadOwnDevices(){
    var deviceGet = 'http://team10.pythonanywhere.com/userDevices/get';
    var deviceList = [];
    var el = document.getElementById('ownDevices');

    var xhr = new XMLHttpRequest();
    xhr.open('GET', deviceGet, true);
    xhr.onload = function() {
        deviceList = JSON.parse(xhr.response);

        //Populate the form with values
        for(var i = 0; i<deviceList.length; i++)
        {
            var node = document.createElement('option');
            node.value = i;
            node.innerHTML = deviceList[i].deviceName;

            el.appendChild(node);
        }
    };
    xhr.send();

    //Clear form
    while (el.firstChild) {
    el.removeChild(el.firstChild);}

}

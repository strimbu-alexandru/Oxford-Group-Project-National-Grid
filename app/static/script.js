var options =[{"text"  : "iPhone","value" : "iPhone", "power": "30", "minutes": "120"},
    {"text"     : "Android","value"    : "Android",	"power":"70", "minutes":"300"},
    {"text"  : "Custom","value" : "Custom", "power":"0", "minutes":"0"}
    ];


function formsubmit(p, m){

    $.ajax('./server/best24h/'+p+'/'+m, {
        success: function(data) {
            writeschedule(data, m)
        }
    });
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


function writeschedule(data, m){
    //Calculate length of single charge
    var hours = m/60;var mins = m%60;
    var plugDate =data.data[2].plugInTime;
    plugDate = plugDate.split("T").pop();
    plugDate = plugDate.substring(0,plugDate.length-1);
    var plugDateShort = plugDate.split(":")[0];
    var plugDateMins = plugDate.split(":")[1];
    var plugDateTime = data.data[2].plugInTime
    plugDateTime[10] = ' '
    plugDateTime[16] = ' '

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

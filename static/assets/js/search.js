(function($) {


	var createPieChart = function(data) {

		var total = data.neg + data.pos + data.neu;
		console.log(data.pos, data.neg, data.neu, total);
		$('#container').highcharts({
	        chart: {
	            plotBackgroundColor: null,
	            plotBorderWidth: null,
	            plotShadow: false,
	            type: 'pie'
	        },
	        title: {
	            text: 'Sentiments Regarding: '+data.namez
	        },
	        tooltip: {
	            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
	        },
	        plotOptions: {
	            pie: {
	                allowPointSelect: true,
	                cursor: 'pointer',
	                dataLabels: {
	                    enabled: true,
	                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
	                    style: {
	                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
	                    }
	                }
	            }
	        },
	        series: [{
	            name: "Sentiments",
	            colorByPoint: true,
	            data: [{
	                name: "Positive",
	                y: data.pos,
	                color:'#00e676'
	            }, {
	                name: "Negative",
	                y: data.neg,
	                sliced: true,
	                selected: true,
	                color:'#c32929'
	            }, {
	                name: "Neutral",
	                y: data.neu,
	                color:'#2C3539'
	            }]
	        }]
	    });


	};

	var createlineChart = function(data){
		var months = data.month;
		var monthvalue = $.map(months,function(key,value) {return key});
		var monthlist = $.map(months,function(key,value) {return value});
		console.log(data.month,monthvalue);
		$('#container2').highcharts({
	        chart: {
	            type: 'spline'
	        },
	        title: {
	            text: 'Monthly Hits on: '+data.namez
	        },
	        subtitle: {
	            text: ''
	        },
	        xAxis: {
		            categories: ['वैशाख','जेष्ठ','असार','श्रावण','भाद्र','असोज','कार्तिक','मंसिर','पुस','माघ','फाल्गुन','चैत्र']
	        },
	        yAxis: {
	            title: {
	                text: 'Count'
	            },
	            labels: {
	                formatter: function () {
	                    return this.value;
	                }
	            }
	        },
	        tooltip: {
	            crosshairs: true,
	            shared: true
	        },
	        plotOptions: {
	            spline: {
	                marker: {
	                    radius: 4,
	                    lineColor: '#666666',
	                    lineWidth: 1
	                }
	            }
	        },
	        series: [{
	            name: data.namez,
	            marker: {
	                symbol: 'circle'
	            },
	            data: monthvalue
	        }]
	    });
	};

	var poslist= function(data){

		var posl = [];
		posl = data.score["positive"];
		$("#pos").empty();
		$.each(posl,function(){
			$("#pos").append($('<li/>').text(this));
		});
		var negl = [];
		negl = data.score["negative"];
		$("#neg").empty();
		$.each(negl,function(){
			$("#neg").append($('<li/>').text(this));
		});
	};


	$(document).ready(function() {
		var elem_a = $('#bmenu li a');
		elem_a.click(function() {
			$('#bmenu li a.selected').removeClass('selected');
			$(this).addClass('selected');
		});

		$('#searchthis').submit(function(event) {
			event.preventDefault();
			// AJAX HERE.

			//Main search-bar 
			$.getJSON('/search', {
				q: $('#namanyay-search-box').val(),
				r: $('#search_nav ul li a.selected').text()
			}, function(response) {
				// parse json.
				console.log(response);
				createPieChart(response)
				createlineChart(response)
				poslist(response)

				$('header#bannerHeader').slideDown();
				$('#bannerLoader').hide();

			});
			$('#banner').slideDown();	
			$('header#bannerHeader').hide();
			$('#bannerLoader').show();
			$('html, body').animate({
				scrollTop: $('#banner').offset().top
			});
			return false;
		});


		//top search-bar
		$('#searchthis-top').submit(function(event) {
			event.preventDefault();
			// AJAX HERE.

			$.getJSON('/search', {
				q: $('#namanyay-search-box-top').val(),
				r: $('#top_box option.selected').text()
			}, function(response) {
				// parse json.
				console.log(response);
				createPieChart(response)
				createlineChart(response)
				poslist(response)
				$('header#bannerHeader').slideDown();
				$('#bannerLoader').hide();

			});
			$('header#bannerHeader').hide();
			$('#bannerLoader').show();
			return false;
		});


		var win = $(window);
		var topBar = $('#topBar');
		var header = $('#header');
		win.scroll(function() {
			if (win.scrollTop() > header.offset().top + header.height()) {
				topBar.fadeIn();
			} else if (topBar.is(':visible')) {
				topBar.fadeOut();
			}
		});
	});
})(jQuery);
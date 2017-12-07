$(function() {
	/**筛选**/
	/*进入筛选*/
	$("#headerFiltrate").click(function() {
		$("#header").hide();
		$("#filtratePage").show();
	});
	/*选择分类*/
	var classifyHeight, classifyListHeight, classify = $(".filtrate-classify-list li.active>a").html();
	$(".filtrate-classify-list li a").click(function() {
		$(".filtrate-classify-list li").removeClass("active");		//取消其他分类的选中状态
		$(this).parent("li").addClass("active");						//给被点击分类标记选中状态
		$(this).next("ul").find("ul").hide();						//关闭被点击分类的孙分类
		$(this).parent("li").siblings("li").children("ul").hide();	//关闭父分类其他同等级类的子分类
		$(this).next("ul").show();									//显示被点击分类的子分类
		classify = $(this).html();									//获取被选中的分类值
		classifyHeight = parseInt($(".filtrate-classify").css("height"));			//获取分类盒子的高度
		classifyListHeight = parseInt($(".filtrate-classify-list").css("height"));//获取分类列表的高度
		if (classifyHeight != classifyListHeight) {								//盒子高度与列表高度不同
			$("#classify").addClass("show");
			$("#classify a span").html("收起");									//显示为可收起
			$(".filtrate-classify").animate({height: classifyListHeight});		//展开或收起盒子
		}
	});
	/*收起&展开分类*/
	$("#classify a").click(function() {
		var classifyState = $(this).find("span").html();
		classifyHeight = parseInt($(".filtrate-classify").css("height"));			//获取分类盒子的高度
		classifyListHeight = parseInt($(".filtrate-classify-list").css("height"));//获取分类列表的高度
		if (classifyState != "收起" && classifyHeight != classifyListHeight) {//展开分类
			$("#classify").addClass("show");
			$("#classify a span").html("收起");
			$(".filtrate-classify").animate({height: classifyListHeight});
		} else if (classifyState == "收起") {//收起分类
			$("#classify").removeClass("show");
			if (classify != "") {//已选分类
				$("#classify a span").html(classify);
			} else {//未选分类
				$("#classify a span").html("展开");
			}
			$(".filtrate-classify").animate({height: 0});
		}
	});
	/*选择收货地*/
	var address = "";
	$(".filtrate-address li a").click(function() {
		var addressLi = $(this).parent("li");
		var addressState = addressLi.hasClass("active");
		if (addressState == true) {
			addressLi.removeClass("active");
			address = "";
		} else {
			addressLi.addClass("active").siblings("li").removeClass("active");
			address = $(this).html();
		}
	});
	/*收起&展开收货地区*/
	$("#address a").click(function() {
		var categoryState = $(this).find("span").html();
		var addressHeight = $(".filtrate-address ul").css("height");
		if (categoryState != "收起") {//展开收货地区
			$("#address").addClass("show");
			$("#address a span").html("收起");
			$(".filtrate-address").animate({height: addressHeight});
		} else {//收起收货地区
			$("#address").removeClass("show");
			if (address == "") {//未选收货地
				address = "全部";
			}
			$("#address a span").html(address);
			$(".filtrate-address").animate({height: 0});
		}
	});
	/*选择其他条件*/
	$(".filtrate-other li label").click(function() {
		var otherLi = $(this).parent("li");
		var conditionState = otherLi.hasClass("active");
		if (conditionState == true) {
			otherLi.removeClass("active");
		} else {
			otherLi.addClass("active");
		}
	});
	/*清空筛选条件*/
	$(".filtrate-reset").click(function() {
		/*清空分类*/
		$("#classify").removeClass("show");
		$("#classify a span").html("展开");
		classify = $(".filtrate-classify-list li.active>a").html();
		$(".filtrate-classify-list li").removeClass("active");
		$(".filtrate-classify-list>li").addClass("active");
		$(".filtrate-classify-list li ul li ul").hide();
		/*收起分类*/
		classifyHeight = parseInt($(".filtrate-classify").css("height"));	
		if (classifyHeight > 0) {
			$(".filtrate-classify").animate({height: 0});
		}
		/*清空价格*/
		$("#minPrice, #maxPrice").val("");
		/*清空收货地*/
		$("#address").removeClass("show");
		$("#address a span").html("展开");
		address = "";
		/*收起收货地*/
		var addressBoxHeight = parseInt($(".filtrate-address ul").css("height"));
		if (addressBoxHeight > 0) {
			$(".filtrate-address").animate({height: 0});
		}
		/*清空已选收货地*/
		$(".filtrate-address ul li").removeClass("active");
		/*清空其他选项*/
		$(".filtrate-other ul li").removeClass("active");
	});
	/*从筛选返回主体页面*/
	$("#filtrateBackContains, .filtrate-submit").click(function() {
		$("#header").show();
		$("#filtratePage").hide();
	});
});
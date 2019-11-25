/*별점 : .score*/
/*출처 : http://codepen.io/naradesign/pen/zxPbOw*/
var starRating = function(){
    var $star = $(".score"),
        $result = $star.find("output>b");
        
          $(document)
        .on("focusin", ".score>.input", 
            function(){
                $(this).addClass("focus");
         })
             
           .on("focusout", ".score>.input", function(){
            var $this = $(this);
            setTimeout(function(){
                  if($this.find(":focus").length === 0){
                       $this.removeClass("focus");
                  }
               }, 100);
          })
      
        .on("change", ".score :radio", function(){
            $result.text($(this).next().text());
          })
        .on("mouseover", ".score label", function(){
            $result.text($(this).text());
        })
        .on("mouseleave", ".score>.input", function(){
            var $checked = $star.find(":checked");
                if($checked.length === 0){
                      $result.text("0");
                    } else {
                      $result.text($checked.next().text());
                }
          });
    };
    
    starRating();
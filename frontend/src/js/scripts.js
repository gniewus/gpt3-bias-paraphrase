(function ($) {
    "use strict"; // Start of use strict

    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
        if (
            location.pathname.replace(/^\//, "") ==
                this.pathname.replace(/^\//, "") &&
            location.hostname == this.hostname
        ) {
            var target = $(this.hash);
            target = target.length
                ? target
                : $("[name=" + this.hash.slice(1) + "]");
            if (target.length) {
                $("html, body").animate(
                    {
                        scrollTop: target.offset().top,
                    },
                    1000,
                    "easeInOutExpo"
                );
                return false;
            }
        }
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $(".js-scroll-trigger").click(function () {
        $(".navbar-collapse").collapse("hide");
    });

    // Activate scrollspy to add active class to navbar items on scroll
    $("body").scrollspy({
        target: "#sideNav",
    });

    var highlite = function () {
        var val = $(this).text()
        val = val.replace(
            /\b(Strong)|\b(Active)|\b(Affectionate)|\b(Adventurous)|\b(Child\w*)|\b(Aggress\w*)|\b(Cheer\w*)|\b(Ambitio\w*)|\b(Commit\w*)|\b(Analy\w*)|\b(Communal)|\b(Assert\w*)|\b(Compassion\w*)|\b(Athlet\w*)|\b(Connect\w*)|\b(Autonom\w*)|\b(Considerate)|\b(Boast\w*)|\b(Cooperat\w*)|\b(Challeng\w*)|\b(Depend\w*)|\b(Compet\w*)|\b(Emotiona\w*)|\b(Confident)|\b(Empath\w*)|\b(Courag\w*)|\b(Feminine)|\b(Decide)|\b(Flatterable)|\b(Decisive)|\b(Gentle)|\b(Decision\w*)|\b(Honest)|\b(Determin\w*)|\b(Interpersonal)|\b(Dominant)|\b(Interdependen\w*)|\b(Domina\w*)|\b(Interpersona\w*)|\b(Force\w*)|\b(Kind)|\b(Greedy)|\b(Kinship)|\b(Headstrong)|\b(Loyal\w*)|\b(Hierarch\w*)|\b(Modesty)|\b(Hostil\w*)|\b(Nag)|\b(Implusive)|\b(Nurtur\w*)|\b(Independen\w*)|\b(Pleasant\w*)|\b(Individual\w*)|\b(Polite)|\b(Intellect\w*)|\b(Quiet\w*)|\b(Lead\w*)|\b(Logic)|\b(Sensitiv\w*)|\b(Masculine)|\b(Submissive)|\b(Objective)|\b(Support\w*)|\b(Opinion)|\b(Sympath\w*)|\b(Outspoken)|\b(Tender\w*)|\b(Persist)|\b(Together\w*)|\b(Principle\w*)|\b(Trust\w*)|\b(Reckless)|\b(Understand\w*)|\b(Stubborn)|\b(Warm\w*)|\b(Superior)|\b(Whin\w*)|\b(Self-confiden\w*)|\b(Yield\w*)/ig,
            "<span class='highlight'>$&</span>")

        
        $(this).replaceWith("<p class='un'>" + val + "</p>")
    }

    $("li.desc p").each(highlite)
  

    function askGPT(paragraphContainer,parent) {
        
        let req = $.post({
                    url: "/api",
                    data: JSON.stringify({
                        "data": paragraphContainer.textContent
                    }),
                    //contentType: "application/json",
                    //dataType: 'json',
                });
        req.done(function (response) {
                    $(paragraphContainer).fadeOut(500)
                    res = JSON.parse(response)

                    $(paragraphContainer)
                        .text(function (index, text) {
                            return res.data;
                        })
                    $(paragraphContainer).map(highlite)
                    $(paragraphContainer).fadeIn(500)
                    $(parent).addClass("changed")
                    tippy(paragraphContainer, {
                        content:`<div class="show" >
                            <button type="button" class="btn btn-primary paraphraseit">Paraphrase it using GPT</button>
                            </div>`,
                        allowHTML: true,
                        hideOnClick: true,
                        trigger: 'mouseenter click focus',
                        delay: [null, 100],
                        interactive: true,

                        onShow(instance) {
                            $(instance.popper).find("button")[0].onclick = function(){
                                var $this = $(this);
                                $this.addClass('disabled').html("Loading...");
                                
                                setTimeout(function(){
                                    $this.removeClass('disabled').html('Paraphrase it using GPT');

                                },1000)
                                askGPT(instance.reference,instance.reference.parentElement)
                            }
                            
                        },
                    });
                })
    }


    tippy('li.desc p', {
        content:`<div class="show" >
        <button type="button" class="btn btn-primary paraphraseit">Paraphrase it using GPT</button>
                    </div>`,
        allowHTML: true,
        hideOnClick: true,
        trigger: 'mouseenter click focus',
        delay: [150, 100],
        interactive: true,

        onShow(instance) {
                console.log(instance.reference);
                $(instance.popper).find("button")[0].onclick = function(){
                    var $this = $(this);
                    $this.addClass('disabled').html("Loading...");
                    
                    setTimeout(function(){
                        $this.removeClass('disabled').html('Paraphrase it using GPT');

                    },1000)
                    askGPT(instance.reference,instance.reference.parentElement)
                }    
            },
    });


})(jQuery); // End of use strict

#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)

# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("March Madness Bracket Generator"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel( 
            helpText(p("Author: Ford Fishman."),
                     p("Generate random bracket for NCAAM tournament using FiveThirtyEight power rankings.")
                    ),
            actionButton("do", "Generate a new bracket"),
            downloadButton("downloadData", "Download results (.csv)"),
            h3("Optional Specifications"),
            fileInput("power", h4("Power Rankings"), multiple = FALSE, 
                      accept = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            textOutput("check")
        ),

        # Show a plot of the generated distribution
        mainPanel(
           h1(textOutput("winner"))
          # dataTableOutput("winner")
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
    
    data <- reactive({
        list(
            power = input$power
        )
        
    })
    
    bracket <- eventReactive(input$do, {
        data_ = data()
        source('generator.R', local=T)
        return(list(winner, df))
    })
    
    output$check <- renderText({
        if (is.null(bracket()))
            return("Error")
        "Bracket generated. Download the .csv to see the full results."
        
    })
    
    output$winner <- renderText({
      bracket()[[1]]


    })
    
    
    output$downloadData <- downloadHandler(
      filename = function() {'random_bracket.csv'},
      content = function(file){ 
        write.csv(bracket()[[2]], file, row.names = F)
        }
    )
    



}

# Run the application 
shinyApp(ui = ui, server = server)

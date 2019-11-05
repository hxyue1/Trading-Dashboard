library(shiny)
library(alphavantager)
library(ggplot2)

ui <-fluidPage(
  textInput("ticker","Asset Ticker"),
  selectInput("freq","Frequency",
              choices = list("Intraday"= "intraday", "Daily"="daily")),
  
  conditionalPanel(
    condition = "input.freq == 'daily'",
    dateRangeInput("range","Date Range:")
  ),
  actionButton("launch","Go!"),
  
  mainPanel(
            plotOutput("price"),
            DT::dataTableOutput("mytable")
            )
  
)

server <- function(input,output) {
  
  observeEvent(input$launch,{
    output$price <-renderPlot({
      ticker <- input$ticker
      av_api_key("RUDBPNS133OPNKY1")
      
      
      if(input$freq == "intraday"){
        data <- data.frame(av_get(symbol=ticker,av_fun="TIME_SERIES_INTRADAY",interval="5min"))
        today <- Sys.Date()
        time <- data$timestamp + 14400
        attr(time,"tzone") <- "Australia/Sydney"
        data$timestamp <- time
        data <- data[c(as.Date(Sys.time()) == as.Date(time)),]
      }
      else if(input$freq == "daily"){
        data <- data.frame(av_get(symbol=ticker,av_fun="TIME_SERIES_DAILY",outputsize="full"))
        data <- data[c(data$volume!=0),]
        data <- data[c(data$timestamp >= input$range[1] & data$timestamp <= input$range[2]),]
      }
      
      ggplot(data=data, aes(x=timestamp,y=close)) + geom_line() + theme_bw()
    })
  })
  
}
shinyApp(ui,server)
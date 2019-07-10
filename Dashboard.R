library(shiny)
library(alphavantager)
library(ggplot2)

ui <-fluidPage(
  textInput("ticker","Asset Ticker"),
  checkboxInput("smooth", "Smooth"),
  selectInput("freq",h3("Frequency"),
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
      else{
        data <- data.frame(av_get(symbol=ticker,av_fun="TIME_SERIES_DAILY"),outputsize="full")
        data <- data[c(data$close!=0),]
      }
      
      ggplot(data=data, aes(x=timestamp,y=close)) + geom_line() + theme_bw()
    })
  })
  
  
  # output$mytable = DT::renderDataTable({
  #   ticker <- input$ticker
  #   av_api_key("RUDBPNS133OPNKY1")
  #   data <- data.frame(av_get(symbol=ticker,av_fun="TIME_SERIES_DAILY"))
  # })
}
shinyApp(ui,server)
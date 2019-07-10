library(shiny)
library(alphavantager)
library(ggplot2)

ui <-fluidPage(
  textInput("ticker","Asset Ticker"),
  
  mainPanel(
            plotOutput("price"),
            DT::dataTableOutput("mytable")
            )
  
)

server <- function(input,output) {
  output$price <-renderPlot({
    
    ticker <- input$ticker
    av_api_key("RUDBPNS133OPNKY1")
    today <- Sys.Date()
    data <- data.frame(av_get(symbol=ticker,av_fun="TIME_SERIES_INTRADAY",interval="5min"))
    time <- data$timestamp + 14400
    attr(time,"tzone") <- "Australia/Sydney"
    data$timestamp <- time
    data <- data[c(as.Date(Sys.time()) == as.Date(time)),]
    ggplot(data=data, aes(x=timestamp,y=open)) + geom_line()
  })
  
  # output$mytable = DT::renderDataTable({
  #   ticker <- input$ticker
  #   av_api_key("RUDBPNS133OPNKY1")
  #   data <- data.frame(av_get(symbol=ticker,av_fun="TIME_SERIES_DAILY"))
  # })
}
shinyApp(ui,server)
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
    data <- data.frame(av_get(symbol=ticker,av_fun="TIME_SERIES_DAILY"))
    ggplot(data=data, aes(x=timestamp,y=close)) + geom_line()
  })
  
  output$mytable = DT::renderDataTable({
    ticker <- input$ticker
    av_api_key("RUDBPNS133OPNKY1")
    data <- data.frame(av_get(symbol=ticker,av_fun="TIME_SERIES_DAILY"))
  })
}
shinyApp(ui,server)
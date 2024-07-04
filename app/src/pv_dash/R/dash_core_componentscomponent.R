# AUTO GENERATED FILE - DO NOT EDIT

#' @export
dash_core_componentscomponent <- function(id=NULL, label=NULL, value=NULL) {
    
    props <- list(id=id, label=label, value=value)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'component',
        namespace = 'pv_dash',
        propNames = c('id', 'label', 'value'),
        package = 'pvDash'
        )

    structure(component, class = c('dash_component', 'list'))
}

# AUTO GENERATED FILE - DO NOT EDIT

export dash_core_components_component

"""
    dash_core_components_component(;kwargs...)

A component component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `label` (String; required): A label that will be printed when this component is rendered.
- `value` (String; optional): The value displayed in the input.
"""
function dash_core_components_component(; kwargs...)
        available_props = Symbol[:id, :label, :value]
        wild_props = Symbol[]
        return Component("dash_core_components_component", "component", "pv_dash", available_props, wild_props; kwargs...)
end


# Changelog

## [1.3.2] - 2021-04-09
### Changed
- Bugfix : NeuroTag's "Fix" button failed if the developer moved or renamed the NextMindSDK folder, or get it from UPM
- Bugfix : Simulation mode on Collider2D with perspective Camera
- Bugfix : shadergraphs triplanar projection was using world space normals instead of local space
- Bugfix : shadergraphs "Constant size" property was creating deformation artefacts on stimulation texture
- Use Gradient on ContactsVisualization instead of 2 colors
- Remove "Screen Ratio" property from Nextmind's shaders. This is now computed automatically
### Added 
- Contact Quality is now visible in the profiler, and accessible through script using Device.GetAverageContactQuality()

## [1.3.1] - 2021-03-23
### Changed
- Bugfix : NeuroTags visibility calculation on World Space Canvases
- Bugfix : OnReleased event is now triggered when destroying/disabling a NeuroTag 

## [1.3.0] - 2021-03-12
### Changed
- First release of UPM packages
- Shaders property OverlayColor has been removed for simplicity sake
- Enhance bluetooth connection stability
- Bugfix : overlay blending was not applied properly
- Bugfix : NeuroManager events callbacks (OnDeviceAvailable/Unavailable & OnDeviceConnected/Disconnected) were not called by the right events
- Bugfix : Simulated feedback was not reset when a target is reassigned
### Added
- UWP platforms support (x86 & ARM64)

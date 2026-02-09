# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.1.1] - 2026-02-09
### Changed
- Use external `hivico` PyPI library for HiVi API communication instead of bundled `hivico.py`
- Integration now declares `hivico>=0.1.0` in manifest; installs automatically when hivico is published to PyPI

## [0.1.0] - 2026-01-20
### Added
- Initial release
- Automatic discovery of HiVi Multi-Room speakers
- Basic playback controls (play, pause, volume)
- Multi-room synchronization support
- Configuration flow implementation
- Media player entity creation for each speaker

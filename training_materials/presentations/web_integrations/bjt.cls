%-------------------------------------------------------------
%  Package : BJT Beamer Theme
%  Author  : Baijayanta
%  Version : 1.0
%  Date    : 2026-07-17
%
%  Description:
%    A clean, modern Beamer theme built on top of the
%    Metropolis theme with customized colors, typography,
%    and layout for academic presentations.
%
%  Repository:
%    https://github.com/Baijayanta21/bjt-beamer-theme
%
%  License:
%    Copyright (c) 2026 Baijayanta.
%    Released under the MIT License.
%-------------------------------------------------------------

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{bjt}[2026/07/17 v1.0 Baijayanta Beamer Class]


% Default options
\PassOptionsToClass{aspectratio=169,10pt}{beamer}

% Forward user options
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{beamer}}
\ProcessOptions\relax

% Load beamer
\LoadClass{beamer}

% Core packages
\RequirePackage{mathtools}   % Loads amsmath
\RequirePackage{amssymb}
\RequirePackage{graphicx}
\RequirePackage{booktabs}
\RequirePackage{tikz}

% Common TikZ libraries
\usetikzlibrary{calc,arrows.meta,positioning}

% extra options
\RequirePackage{xparse}

% Insert customized theme bjt
\RequirePackage{bjt/bjttheme}

\endinput
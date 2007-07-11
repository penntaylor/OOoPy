#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************

import sys
from optparse          import OptionParser
from ooopy.OOoPy       import OOoPy
from ooopy.Transformer import split_tag

def cleantag (tag) :
    return ':'.join (split_tag (tag))

def pretty (n, indent = 0, with_text = False) :
    s = ["    " * indent]
    s.append (cleantag (n.tag))
    attrkeys = n.attrib.keys ()
    attrkeys.sort ()
    for a in attrkeys :
        s.append (' %s="%s"' % (cleantag (a), n.attrib [a]))
    if with_text and n.text is not None :
        s.append (' TEXT="%s"' % n.text)
    if with_text and n.tail is not None :
        s.append (' TAIL="%s"' % n.tail)
    print ''.join (s).encode ('utf-8')
    for sub in n :
        pretty (sub, indent + 1, with_text)

if __name__ == '__main__' :
    usage  = "%prog [-f|--file <xml-file>] [-t|--with-text] file ..."
    parser = OptionParser (usage = usage)
    parser.add_option \
        ( "-f", "--file"
        , dest = "ooofile"
        , help = "XML-File inside OOo File"
        , default = 'content.xml'
        )
    parser.add_option \
        ( "-t", "--with-text"
        , dest    = "with_text"
        , action  = "store_true"
        , help    = "Print text of xml nodes"
        , default = False
        )
    (options, args) = parser.parse_args ()
    if len (args) < 1 :
        parser.print_help (sys.stderr)
        sys.exit (23)
    for f in args :
        o = OOoPy (infile = f)
        e = o.read (options.ooofile)
        pretty (e.getroot (), with_text = options.with_text)
        o.close ()

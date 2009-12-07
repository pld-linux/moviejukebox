%define		svnrev	1232
%include	/usr/lib/rpm/macros.java
Summary:	moviejukebox
Name:		moviejukebox
Version:	1.7
Release:	0.%{svnrev}.1
License:	GPL v3
Group:		Applications
# svn export http://moviejukebox.googlecode.com/svn/trunk/moviejukebox
# rm lib/commons-collections*jar lib/commons-logging*jar lib/commons-lang*jar lib/junit*jar
Source0:	http://xatka.net/~z/PLD/%{name}-r%{svnrev}.tar.bz2
# Source0-md5:	013170c09dbc2ba94409b5075d7430e8
URL:		http://code.google.com/p/moviejukebox/
BuildRequires:	java-commons-collections
BuildRequires:	java-commons-lang >= 2.4
BuildRequires:	java-commons-logging
BuildRequires:	java-junit >= 4.5
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
Requires:	java-commons-collections
Requires:	java-commons-lang >= 2.4
Requires:	java-commons-logging
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
moviejukebox

%prep
%setup -qn %{name}-r%{svnrev}

cat > moviejukebox.sh << EOF
#!/bin/sh
. %{_datadir}/java-utils/java-functions
mkdir -p \$HOME/.moviejukebox
CLASSPATH=\$HOME/.moviejukebox:%{_datadir}/%{name}:\$(build-classpath-directory %{_javadir}/%{name})
set_javacmd
\$JAVACMD -Xms256m -Xmx512m -cp \$CLASSPATH com.moviejukebox.MovieJukebox "\$@"
EOF

chmod a+x %{name}.sh

%build

CLASSPATH=$(build-classpath commons-lang commons-collections commons-logging junit)

%ant -Dbuild.sysclasspath=first

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
install -d $RPM_BUILD_ROOT%{_bindir}

cp -a dist/lib $RPM_BUILD_ROOT%{_javadir}/%{name}
cp -a dist/properties $RPM_BUILD_ROOT%{_datadir}/%{name}/properties
cp -a dist/skins $RPM_BUILD_ROOT%{_datadir}/%{name}/skins
install %{name}.sh $RPM_BUILD_ROOT%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_javadir}/%{name}
%{_datadir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}

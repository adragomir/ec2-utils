%define _buildid %{nil}

%bcond_without upstart

%define with_systemd 1
%undefine with_upstart

Name:      ec2-utils
Summary:   A set of tools for running in EC2
Version:   0.6
Release:   2%{?_buildid}%{?dist}
License:   Apache License 2.0
Group:     System Tools
Source0:   ec2-metadata
Source1:   ec2udev-vbd
Source2:   51-ec2-hvm-devices.rules
Source3:   52-ec2-vcpu.rules
Source4:   53-ec2-network-interfaces.rules
Source5:   75-persistent-net-generator.rules
Source6:   ec2net-functions
Source7:   ec2net.hotplug
Source8:   ec2ifup
Source9:   ec2ifdown
Source10:  ec2dhcp.sh
Source11:  ec2ifup.8
Source12:  ec2ifscan
Source13:  elastic-network-interfaces.conf
Source14:  ec2ifscan.8
Source15:  ec2udev-vcpu

Source20:  ixgbevf.conf
Source21:  acpiphp.modules

# centos stuff
Source30:  elastic-network-interfaces.service
Source31:  ec2-ifup@.service

URL:       http://developer.amazonwebservices.com/connect/entry.jspa?externalID=1825
BuildArch: noarch
Provides:  ec2-metadata
Obsoletes: ec2-metadata
Requires:  curl
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
ec2-utils contains a set of utilities for running in ec2.

%package -n ec2-net-utils
Summary:   A set of network tools for managing ENIs
Group:     System Tools
Requires:  initscripts
Requires:  bash >= 4
Requires:  curl
Requires:  iproute
%if %{with upstart}
Requires:  upstart
%endif
%if %{with systemd}
BuildRequires: systemd-units
%endif

%description -n ec2-net-utils
ec2-net-utils contains a set of utilities for managing elastic network
interfaces.

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/local/bin
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/dhcp/dhclient.d/
%if %{with upstart}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/init/
%endif
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8/

install -m755 %{SOURCE0} $RPM_BUILD_ROOT/usr/local/bin/
%if ! %{?centos}
install -m755 %{SOURCE1} $RPM_BUILD_ROOT/sbin/
%endif
install -m755 %{SOURCE8} $RPM_BUILD_ROOT/sbin/
install -m755 %{SOURCE9} $RPM_BUILD_ROOT/sbin/
install -m755 %{SOURCE12} $RPM_BUILD_ROOT/sbin/
%if ! %{?centos}
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
install -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
%endif
install -m644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
%if %{with upstart}
install -m644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
%endif
install -m644 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts/
install -m755 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts/
install -m755 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/dhcp/dhclient.d/
%if %{with upstart}
install -m644 %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/init
%endif
install -m644 %{SOURCE11} $RPM_BUILD_ROOT%{_mandir}/man8/ec2ifup.8
ln -s ./ec2ifup.8.gz $RPM_BUILD_ROOT%{_mandir}/man8/ec2ifdown.8.gz
install -m644 %{SOURCE14} $RPM_BUILD_ROOT%{_mandir}/man8/ec2ifscan.8

%if %{with systemd}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{_unitdir}
%{__install} -m 0644 %{SOURCE30} ${RPM_BUILD_ROOT}%{_unitdir}
%{__install} -m 0644 %{SOURCE31} ${RPM_BUILD_ROOT}%{_unitdir}
%endif

# add module configs
install -m644 -D %{SOURCE20} $RPM_BUILD_ROOT/etc/modprobe.d/ixgbevf.conf
install -m755 -D %{SOURCE21} $RPM_BUILD_ROOT/etc/sysconfig/modules/acpiphp.modules

%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/local/bin/ec2-metadata
%if ! %{?centos}
/sbin/ec2udev-vbd
/sbin/ec2udev-vcpu
%{_sysconfdir}/udev/rules.d/51-ec2-hvm-devices.rules
%{_sysconfdir}/udev/rules.d/52-ec2-vcpu.rules
%endif

%files -n ec2-net-utils
/sbin/ec2ifup
/sbin/ec2ifdown
/sbin/ec2ifscan
%{_sysconfdir}/udev/rules.d/53-ec2-network-interfaces.rules
%if %{with upstart}
%{_sysconfdir}/udev/rules.d/75-persistent-net-generator.rules
%endif
%{_sysconfdir}/modprobe.d/ixgbevf.conf
%{_sysconfdir}/sysconfig/modules/acpiphp.modules
%{_sysconfdir}/sysconfig/network-scripts/ec2net-functions
%{_sysconfdir}/sysconfig/network-scripts/ec2net.hotplug
%{_sysconfdir}/dhcp/dhclient.d/ec2dhcp.sh
%if %{with upstart}
%{_sysconfdir}/init/elastic-network-interfaces.conf
%endif
%{_mandir}/man8/ec2ifup.8.gz
%{_mandir}/man8/ec2ifdown.8.gz
%{_mandir}/man8/ec2ifscan.8.gz

%if %{with systemd}
%{_unitdir}/elastic-network-interfaces.service
%{_unitdir}/ec2-ifup@.service
%endif

%if %{with systemd}
%post -n ec2-net-utils
%systemd_post elastic-network-interfaces.service
%systemd_post ec2-ifup@.service

%preun -n ec2-net-utils
%systemd_preun elastic-network-interfaces.service
%systemd_preun ec2-ifup@.service

%postun -n ec2-net-utils
%systemd_postun elastic-network-interfaces.service
%systemd_postun ec2-ifup@.service
%endif

%changelog
* Thu May 8 2014 Ben Cressey <bcressey@amazon.com>
- delay running ec2ifscan until after udev-post

* Fri Apr 11 2014 Ethan Faust <efaust@amazon.com>
- don't bring up vcpus automatically if maxcpus is set

* Fri Jan 10 2014 Ben Cressey <bcressey@amazon.com>
- Do not use DNS settings from secondary interfaces by default

* Tue Sep 24 2013 Andrew Jorgensen <ajorgens@amazon.com>
- Add hotplug script and module config

* Mon Aug 26 2013 Ben Cressey <bcressey@amazon.com>
- Configure interfaces attached at launch time

* Wed Mar 13 2013 Andrew Jorgensen <ajorgens@amazon.com>
- Use -q to avoid using a user's .curlrc

* Sun Sep 16 2012 Ben Cressey <bcressey@amazon.com>
- Add documentation for ec2ifup and ec2ifdown

* Thu Sep 13 2012 Ben Cressey <bcressey@amazon.com>
- Optimize metadata queries for elastic interfaces

* Tue Sep 11 2012 Ben Cressey <bcressey@amazon.com>
- Adjust route table usage for elastic interfaces
- Update headers to reflect Apache 2.0 license

* Wed Sep 5 2012 Ben Cressey <bcressey@amazon.com>
- Configure elastic network interfaces via DHCP

* Wed Aug 29 2012 Andrew Jorgensen <ajorgens@amazon.com>
- Add dependency on curl for ec2-metadata
- Update ec2-metadata to 0.1.1 bugfix release

* Mon Aug 13 2012 Ben Cressey <bcressey@amazon.com>
- Add rules and scripts for MultiIP / MultiVIF support

* Mon Jul 30 2012 Ethan Faust <efaust@amazon.com>
- Added udev rules to automatically bring up vCPUs when they're added.

* Mon Aug 1 2011 Nathan Blackham <blackham@amazon.com>
- adding BuildRoot directive to specfile.

* Wed Sep 22 2010 Nathan Blackham <blackham@amazon.com>
- move to ec2-utils
- add udev code for symlinking xvd* devices to sd*
- fixing typo in spec file
- adding udev symlinks for xvd* devices

* Tue Sep 07 2010 Nathan Blackham <blackham@amazon.com>
- initial packaging of script as an rpm
- moving rpm to noarch
- adding Group line in specfile
- initial packaging of ec2-metadata
- setup complete for package ec2-metadata

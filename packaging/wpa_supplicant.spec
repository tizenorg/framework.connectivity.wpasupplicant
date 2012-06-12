Name:           wpa_supplicant
Version:        0.8.0
Release:        8
License:        BSD license
Summary:        Support for WPA and WPA2 (IEEE 802)
Group:          System/Network
Source0:        %{name}-%{version}.tar.gz
Source1001:     wpasupplicant.manifest

BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libnl-2.0)
BuildRequires:  pkgconfig(libssl)
BuildRequires:  pkgconfig(openssl)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
WPA and WPA2 are methods for securing wireless networks, the former
using IEEE 802.1X, and the latter using IEEE 802.11i. This software
provides key negotiation with the WPA Authenticator, and controls
association with IEEE 802.11i networks.

%prep
%setup -q

%build
cp %{SOURCE1001} .
cp -v configurations/tizen.config wpa_supplicant/.config
cd wpa_supplicant
make %{?_smp_mflags} all

%install
mkdir -p %{buildroot}%{_sbindir}/systemd/
mkdir -p %{buildroot}%{_sbindir}/dbus/
cd wpa_supplicant
%make_install

# D-Bus
mkdir -p %{buildroot}%{_prefix}/etc/dbus-1/system.d/
cp dbus/dbus-wpa_supplicant.conf %{buildroot}%{_prefix}/etc/dbus-1/system.d/wpa_supplicant.conf
mkdir -p %{buildroot}%{_datadir}/dbus-1/services/
cp dbus/fi.epitest.hostap.WPASupplicant.service %{buildroot}%{_datadir}/dbus-1/services/
cp dbus/fi.w1.wpa_supplicant1.service %{buildroot}%{_datadir}/dbus-1/services/

mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
cp ../etc/rc.d/init.d/wpa_supplicant %{buildroot}%{_sysconfdir}/rc.d/init.d/wpa_supplicant
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/rc3.d/
ln -s ../init.d/wpa_supplicant %{buildroot}%{_sysconfdir}/rc.d/rc3.d/S62wpasupplicant
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/rc5.d/
ln -s ../init.d/wpa_supplicant %{buildroot}%{_sysconfdir}/rc.d/rc5.d/S62wpasupplicant

# sanitise the example configuration
mkdir -p %{buildroot}%{_datadir}/doc/wpasupplicant
sed 's/^\([^#]\+=.*\|}\)/#\1/' < ./wpa_supplicant.conf | gzip > %{buildroot}%{_datadir}/doc/wpasupplicant/README.wpa_supplicant.conf.gz

rm -rf %{buildroot}%{_sbindir}/systemd/
rm -rf %{buildroot}%{_sbindir}/dbus/
rm -rf %{buildroot}%{_sbindir}/wpa_passphrase

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest wpasupplicant.manifest
%{_sbindir}/wpa_cli
%{_sbindir}/wpa_supplicant
%attr(644,-,-) %{_prefix}/etc/dbus-1/system.d/*.conf
%attr(644,-,-) %{_datadir}/dbus-1/services/*.service
%{_defaultdocdir}/wpasupplicant/README.wpa_supplicant.*
%{_sysconfdir}/rc.d/init.d/wpa_supplicant
%{_sysconfdir}/rc.d/rc3.d/S62wpasupplicant
%{_sysconfdir}/rc.d/rc5.d/S62wpasupplicant

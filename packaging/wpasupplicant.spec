#sbs-git:pkgs/w/wpasupplicant

Name:	    wpasupplicant
Summary:    Support for WPA and WPA2 (IEEE 802.11i / RSN)
Version:    0.8.0
Release:    7
Group:      System/Network
License:    BSD license
Source0:    %{name}-%{version}.tar.gz
Source1:        wpa_supplicant.service
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(libssl)
BuildRequires: pkgconfig(libcrypto)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(libnl-2.0)

%description
WPA and WPA2 are methods for securing wireless networks, the former
using IEEE 802.1X, and the latter using IEEE 802.11i. This software
provides key negotiation with the WPA Authenticator, and controls
association with IEEE 802.11i networks.

%prep
%setup -q

%build
cp -v configurations/tizen.config wpa_supplicant/.config
cp -v configurations/tizen_hostapd.config hostapd/.config
make %{?_smp_mflags} -C wpa_supplicant all
make %{?_smp_mflags} -C hostapd all

%install
mkdir -p %{buildroot}%{_sbindir}/systemd/
mkdir -p %{buildroot}%{_sbindir}/dbus/

cp -v wpa_supplicant/wpa_supplicant %{buildroot}%{_sbindir}/
cp -v wpa_supplicant/wpa_cli %{buildroot}%{_sbindir}/
cp -v hostapd/hostapd %{buildroot}%{_sbindir}/
cp -v hostapd/hostapd_cli %{buildroot}%{_sbindir}/

# Configurations
mkdir -p %{buildroot}%{_sysconfdir}/wpa_supplicant/
cp -v wpa_supplicant/wpa_supplicant.conf %{buildroot}%{_sysconfdir}/wpa_supplicant/wpa_supplicant.conf
cp -v hostapd/hostapd.conf %{buildroot}%{_sysconfdir}/wpa_supplicant/hostapd.conf

# D-Bus
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d/
cp wpa_supplicant/dbus/dbus-wpa_supplicant.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/wpa_supplicant.conf
mkdir -p %{buildroot}%{_datadir}/dbus-1/services/
cp wpa_supplicant/dbus/fi.epitest.hostap.WPASupplicant.service %{buildroot}%{_datadir}/dbus-1/services/
cp wpa_supplicant/dbus/fi.w1.wpa_supplicant1.service %{buildroot}%{_datadir}/dbus-1/services/

mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
cp etc/rc.d/init.d/wpa_supplicant %{buildroot}%{_sysconfdir}/rc.d/init.d/wpa_supplicant
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/rc3.d/
ln -s ../init.d/wpa_supplicant %{buildroot}%{_sysconfdir}/rc.d/rc3.d/S62wpasupplicant
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/rc5.d/
ln -s ../init.d/wpa_supplicant %{buildroot}%{_sysconfdir}/rc.d/rc5.d/S62wpasupplicant

# sanitise the example configuration
mkdir -p %{buildroot}%{_defaultdocdir}/wpasupplicant
sed 's/^\([^#]\+=.*\|}\)/#\1/' < ./wpa_supplicant/wpa_supplicant.conf | gzip > %{buildroot}%{_defaultdocdir}/wpasupplicant/README.wpa_supplicant.conf.gz

# install systemd service file
mkdir -p %{buildroot}%{_libdir}/systemd/system
install -m 0644 %{SOURCE1} %{buildroot}%{_libdir}/systemd/system/
mkdir -p %{buildroot}%{_libdir}/systemd/system/network.target.wants
ln -s ../wpa_supplicant.service %{buildroot}%{_libdir}/systemd/system/network.target.wants/wpa_supplicant.service

rm -rf %{buildroot}%{_sbindir}/systemd/
rm -rf %{buildroot}%{_sbindir}/dbus/
rm -rf %{buildroot}%{_sbindir}/wpa_passphrase

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_sbindir}/wpa_cli
%{_sbindir}/wpa_supplicant
%{_sbindir}/hostapd
%{_sbindir}/hostapd_cli
%attr(644,-,-) %{_sysconfdir}/dbus-1/system.d/*.conf
%attr(644,-,-) %{_datadir}/dbus-1/services/*.service
%attr(644,-,-) %{_sysconfdir}/wpa_supplicant/*.conf
%{_defaultdocdir}/wpasupplicant/README.wpa_supplicant.*
%{_sysconfdir}/rc.d/init.d/wpa_supplicant
%{_sysconfdir}/rc.d/rc3.d/S62wpasupplicant
%{_sysconfdir}/rc.d/rc5.d/S62wpasupplicant
%{_libdir}/systemd/system/wpa_supplicant.service
%{_libdir}/systemd/system/network.target.wants/wpa_supplicant.service

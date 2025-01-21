import 'package:flutter/material.dart';
import 'screens/home/home_screen.dart'; // Update path as per your structure
import 'screens/profile/profile_screen.dart'; // Example
import 'screens/settings/settings_screen.dart'; // Example

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const HomeScreen(),
        '/profile': (context) => const ProfileScreen(), // Example
        '/settings': (context) => const SettingsScreen(), // Example
      },
    );
  }
}

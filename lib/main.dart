import 'package:flutter/material.dart';
import 'screens/home/home_screen.dart';
import 'screens/profile/profile_screen.dart';
import 'screens/settings/settings_screen.dart';
import 'screens/login/login_screen.dart';
import 'screens/register/register_screen.dart'; // Import RegisterScreen

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AquaPlus',
      theme: ThemeData(
        primarySwatch: Colors.teal, // Aqua blue theme
        colorScheme: ColorScheme.fromSwatch(
          primarySwatch: Colors.teal,
        ).copyWith(
          secondary: Color.fromARGB(255, 23, 192, 230), // Aqua blue
        ),
        textTheme: const TextTheme(
          bodyMedium: TextStyle(color: Colors.black), // Updated to bodyMedium
        ),
      ),
      initialRoute: '/login', // Start with the login page
      routes: {
        '/login': (context) => const LoginScreen(),
        '/home': (context) => const HomeScreen(),
        '/profile': (context) => const ProfileScreen(),
        '/settings': (context) => const SettingsScreen(),
        '/register': (context) =>
            const RegisterScreen(), // Add RegisterScreen route
      },
    );
  }
}
